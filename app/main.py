from flask import Flask, redirect, url_for, render_template, flash, request, send_from_directory

from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user, login_required, login_manager


from app.client import MyClient
from app.client import getWebAPI
from app.analyser import Analyser
from app.user import User


api = MyClient()
app = Flask(__name__)
app.secret_key = 'super secret key'
# login_manager = LoginManager(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route("/policy")
def policy_view():
    return render_template('policy.html', title='Privacy policy')


@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html', title='Welcome')

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/stats', methods=['GET', 'POST'])
# @login_required
def stats():
    return render_template('stats.html', title='Stats')

@app.route('/stats/personal', methods=['GET', 'POST'])
# @login_required
def personal_stats():
    error = user.username
    # if request.method == 'POST':
        # login = request.form['username']
    return render_template('stats/personal.html', error=error)

@app.route('/stats/user', methods=['GET', 'POST'])
# @login_required
def user_enter_stats():
    if request.method == 'POST':
        login = request.form['username']
        date_from = request.form['from']
        date_to = request.form['to']
        return redirect(url_for('user_stats', username=login, date_from=date_from, date_to=date_to))
    return render_template('stats/user.html')


@app.route('/stats/<username>')
# @login_required
def user_stats(username, date_from, date_to):
    return render_template('stats/username.html', name=username)

@app.route('/premium', methods=['GET', 'POST'])
# @login_required
def premium():
    if request.method == 'POST':
        flash('You are Premium user now!')
    return render_template('premium.html', title='Premium')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        try:
            api = getWebAPI(login, password)
            if api.is_authenticated:
                 return redirect('/stats')
            else:
                error = 'Failed to login. Please, try again.'
        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            error = 'Invalid Credentials. Please try again.'
            

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
