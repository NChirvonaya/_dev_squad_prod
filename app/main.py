from flask import Flask, redirect, url_for, render_template, flash, request, send_from_directory

from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user, login_required, login_manager


from app.client import MyClient
from app.client import getWebAPI
from app.analyser import Analyser
from app.user import User

import json
from dataclasses import dataclass, asdict

api = MyClient()
app = Flask(__name__)
app.secret_key = 'super secret key'
# login_manager = LoginManager(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory('js', path)

# @app.route('/css/<path:path>')
# def send_css(path):
#     return send_from_directory('css', path)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/policy")
def policy_view():
    return render_template('policy.html', title='Privacy policy')


@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html', title='Welcome')

@app.route('/logout')
# @login_required
def logout():
    # logout_user()
    return redirect(url_for('index'))

@dataclass
class Resp:
    w_com: int = 0
    wt_com: int = 1
    post_pos: int = 2
    post_neg: int = 3
    post_neu: int = 4
    com_all: int = 5
    com_pos: int = 6
    com_neg: int = 7
    com_neu: int = 8
    com_unq: int = 9

@app.route('/stats', methods=['GET', 'POST'])
# @login_required
def stats():
    # if request.method == 'POST':
    #     error = None
    #     login = request.form['username']
    #     if login is None or login == '':
    #         error = 'Empty username'
    #         return render_template('stats.html', title='Stats', error = error)
    #     date_from = request.form['from']
    #     date_to = request.form['to']
    #     resp = Resp()
    #     return redirect(
    #         url_for(
    #             'user_stats',
    #             response_cur=json.dumps(
    #                 asdict(resp)
    #             ), 
    #             username=login, 
    #             date_from=date_from, 
    #             date_to=date_to
    #         )
    #     )
    return render_template('stats.html', title='Stats')

# @app.route('/stats/personal', methods=['GET', 'POST'])
# # @login_required
# def personal_stats():
#     # error = user.username
#     # if request.method == 'POST':
#         # login = request.form['username']
#     response_cur = request.args['response_cur']
#     resp_dict = json.loads(response_cur)
#     response_cur = Resp(**resp_dict)
#     print(response_cur)
    
#     return render_template('stats/personal.html', resp=response_cur)

@app.route('/stats/profile', methods=['GET', 'POST'])
# @login_required
def profile_stats():
    if request.method == 'POST':
        error = None
        login = request.form['username']
        if login is None or login == '':
            error = 'Empty username'
            return render_template('profile.html', title='Stats', error=error)
        date_from = request.form['from']
        date_to = request.form['to']
        resp = Resp()
        return redirect(
            url_for(
                'user_stats',
                response_cur=json.dumps(
                    asdict(resp)
                ),
                username=login,
                date_from=date_from,
                date_to=date_to
            )
        )
    return render_template('stats/profile.html', title='Stats')


@app.route('/stats/profile/<username>')
# @login_required
def user_stats(
        username, 
        # date_from, 
        # date_to
):
    print("Args:", request.args)
    date_from = request.args['date_from']
    date_to = request.args['date_to']
    response_cur = request.args['response_cur']
    resp_dict = json.loads(response_cur)
    response_cur = Resp(**resp_dict)
    return render_template('stats/personal.html', name=username, resp=response_cur)

# @app.route('/premium', methods=['GET', 'POST'])
# # @login_required
# def premium():
#     if request.method == 'POST':
#         flash('You are Premium user now!')
#     return render_template('premium.html', title='Premium')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        return redirect('/stats')
        # try:
        #     api = getWebAPI(login, password)
        #     if api.is_authenticated:
        #         return redirect('/stats')
        #     else:
        #         error = 'Failed to login. Please, try again.'
        # except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        #     error = 'Invalid Credentials. Please try again.'
            

        # api = InstagramAPI(login, password)
        # api.USER_AGENT = 'Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
        # if (api.login()):
        #     api.getSelfUserFeed()  # get self user feed
        #     print(api.LastJson)  # print last response JSON
        #     print("Login succes!")
        #     return redirect('/stats')
        # else:
        #     print("Can't login!")
        #     error = 'Invalid Credentials. Please try again.'

        # if login != 'admin' or password != 'admin':
        #     error = 'Invalid Credentials. Please try again.'
        # else:
        #     return redirect('/stats')
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
