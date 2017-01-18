from flask import Flask, render_template, session, redirect
from twitter_utils import get_request_token, get_oauth_verifier_url

app = Flask(__name__)
app.secret_key = '1234'
# this is necessary so that the cookies can be encrypted and secured

@app.route('/') # means http://127.0.0.1:4995
# decorator. means when meet / - return the contents of the method below
def homepage():
    return render_template('home.html')

# app route can have smth like /users. So when they are at the user endpoint
# then the method below will be executed and a certain page will be displayed

@app.route('/login/twitter')
def twitter_login():
    request_token = get_request_token()
    # this var is inside the method and will disappear after leaving the func
    # but we need this var later. The way to use it - sessions and cookies
    session['request_token'] = request_token
    # session is persistent between the requests

    # cookie gets stored in the browser of the user. Flask will now that this cookie is related to a certain session
    # session is stored on a hard-drive. And it contains the request token

    return redirect(get_oauth_verifier_url(request_token))


    # redirecting the user to twitter

app.run(port=4995)
