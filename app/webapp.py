"""Declare Flask routes."""
import os
from urllib.parse import urlparse

from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    send_from_directory,
)
from flask_login import current_user, login_required, login_user, logout_user

from werkzeug.urls import url_parse

from app.extensions import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User

from app.analytics import (
    InstAnalytics,
    PostStats,
    ProfileStats,
)

import json

server_bp = Blueprint("main", __name__)


ANALYTICS = InstAnalytics()


@server_bp.route("/favicon.ico")
def favicon():
    """Loads favicon."""
    return send_from_directory(
        os.path.join(server_bp.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@server_bp.errorhandler(404)
def page_not_found(error):
    """404 page."""
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


# @server_bp.route("/policy")
# def policy_view():
#     return render_template('policy.html', title='Privacy policy')


@server_bp.route("/", methods=["POST", "GET"])
def index():
    """Home page."""
    return render_template("index.html", title="Welcome")


@server_bp.route("/login/", methods=["GET", "POST"])
def login():
    """Authenticate user."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = "Invalid username or password"
            return render_template("login.html", form=form, error=error)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@server_bp.route("/logout/")
@login_required
def logout():
    """Unauthenticate user."""
    logout_user()

    return redirect(url_for("main.index"))


@server_bp.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("main.login"))
    except Exception:
        error = "This user already exists"
        return render_template(
            "register.html", title="Register", form=form, error=error
        )

    return render_template("register.html", title="Register", form=form)


@server_bp.route("/error", methods=["GET", "POST"])
def error_page():
    """Stats homepage."""
    error = request.args.get("error")
    return render_template("error.html", title="Error", error=error)


@server_bp.route("/stats", methods=["GET", "POST"])
@login_required
def stats():
    """Stats homepage."""
    return render_template("stats.html", title="Stats")


@server_bp.route("/stats/profile", methods=["GET", "POST"])
@login_required
def profile_stats():
    if request.method == "POST":
        error = None
        login = request.form["username"]
        from_date = request.form["from"]
        to_date = request.form["to"]
        if login is None or login == "":
            error = "Empty username"
            return render_template(
                "stats/profile.html", title="Stats", error=error
            )
        return redirect(
            url_for(
                "main.user_stats",
                username=login,
                from_date=from_date,
                to_date=to_date,
            )
        )
    return render_template("stats/profile.html", title="Stats")


@server_bp.route("/stats/profile/<username>")
@login_required
def user_stats(username):
    search_from = request.args["from_date"]
    search_to = request.args["to_date"]
    results = ANALYTICS.get_profile_results(username, search_from, search_to)

    print("dates", search_from, search_to)
    if not results:
        ANALYTICS.get_profile_results(username)
        return render_template("stats/wait.html")
    else:
        return redirect(
            url_for(
                "main.user_stats_results",
                json=json.dumps(results),
                username=username,
            ),
            307,
        )


@server_bp.route("/stats/profile/<username>/_ready")
@login_required
def user_stats__ready(username):
    result = ANALYTICS.get_profile_results(username)
    if not result:
        return {"ready": False}
    elif result.get("error"):
        return {"ready": False, "error": result["error"]}
    else:
        return {"ready": True}


@server_bp.route("/stats/profile/<username>/results")
@login_required
def user_stats_results(username):
    response_cur = request.args["json"]
    resp_dict = json.loads(response_cur)
    response_cur = ProfileStats(**resp_dict)
    return render_template(
        "stats/personal.html", name=username, resp=response_cur
    )


@server_bp.route("/stats/post", methods=["GET", "POST"])
@login_required
def post_stats():
    if request.method == "POST":
        error = None
        url = request.form["url"]
        if url is None or url == "":
            error = "Empty url"
            return render_template(
                "stats/post.html", title="Stats", error=error
            )
        try:
            post_link = urlparse(url).path.split("/")[2]
            return redirect(
                url_for("main.post_link_stats", post_link=post_link)
            )
        except Exception:
            error = (
                "Please use this format: http://www.instagram.com/p/<postID>"
            )
            return render_template(
                "stats/post.html", title="Stats", error=error
            )
    return render_template("stats/post.html", title="Stats")


@server_bp.route("/stats/_check_user/<user>", methods=["GET", "POST"])
def _check_user(user):
    return ANALYTICS._get_user_id(user)


@server_bp.route("/stats/post/<post_link>")
@login_required
def post_link_stats(post_link):
    post_link = post_link
    results = ANALYTICS.get_post_results(post_link)
    if not results:
        ANALYTICS.get_post_results(post_link)
        return render_template("stats/wait.html")
    else:
        return redirect(
            url_for(
                "main.post_link_stats_results",
                json=json.dumps(results),
                post_link=post_link,
            ),
            307,
        )


@server_bp.route("/stats/post/<post_link>/_ready")
@login_required
def post_link_stats__ready(post_link):
    """Top secret page."""
    result = ANALYTICS.get_post_results(post_link)
    if not result:
        return {"ready": False}
    elif result.get("error"):
        return {"ready": False, "error": result["error"]}
    else:
        return {"ready": True}


@server_bp.route("/stats/post/<post_link>/results")
@login_required
def post_link_stats_results(post_link):
    post_link = post_link
    response_cur = request.args["json"]
    resp_dict = json.loads(response_cur)
    response_cur = PostStats(**resp_dict)
    return render_template(
        "stats/publication.html", name=post_link, resp=response_cur
    )


# @server_bp.route('/premium', methods=['GET', 'POST'])
# @login_required
# def premium():
#     if request.method == 'POST':
#         flash('You are Premium user now!')
#     return render_template('premium.html', title='Premium')
