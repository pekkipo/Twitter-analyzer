import constants
import oauth2
import urllib.parse as urlparse # as just renames it
import json
from user import User
from database import Database

# Create consumer to identify the app
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

Database.initialize(user='postgres', password='1234', host='localhost', database='Learning')

user_email = input('Enter your email: ')

user = User.load_from_db_by_email(user_email)

if user: # if user exists, i.e. statement above has given some result from the DB
    pass
else:

    # create a client to perform a request for the request token
    client = oauth2.Client(consumer)

    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    # left - what the request returns
    # first request
    # refer to the order in the course
    if response.status != 200: # 200 is everything's fine
        print("An error occured when getting the request token from Twitter")

    # Get the request token parsing the query string returned
    request_token  = dict(urlparse.parse_qsl(content.decode('utf-8')))
    # content is in a format of query string parameter
    # we convert it into a dictionary
    # decode converts bytes to strings
    # this is indeed more readable then the original request result without dict convertion


    # Steps afterwards
    # Press Sign up with twitter button on my web-site
    # user presses sign up on twitter web-site
    # Twitter sends back to my web-site/auth
    # I get the auth code + request token -> twitter -> access token

    # Ask the user
    # We are doing Pin auth. Just for learning purpose. We have a console application
    print("Go to the following web-site:")
    print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))
    # {} will be replaced by two variables
    # request_token is a dictionary
    # user gets the pin from the web-page

    # User must type the pin
    oauth_verifier = input("What is the pin? ")

    # Create a token object which contains the request token and the verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    client = oauth2.Client(consumer, token)

    # We use this client to get an access token
    # Ask Twitter for a request token and Twitter knows it should give us it because we verified the request token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    access_token  = dict(urlparse.parse_qsl(content.decode('utf-8')))

    print(access_token)

    first_name = input('Enter name ')
    last_name = input('Enter surname ')

    # Create user
    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()



# Create an authenticated Token object and use it to perform Twitter API calls on behalf of the user
authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
# by that time we surely have a user. Either the one loaded from DB (has tokens already) or the one that was just created

authorized_client = oauth2.Client(consumer, authorized_token)

# Make Twitter API calls
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')
# see REST API section on twitter docs
# search computer related tweets (but images)
# search term comes after ?q=

if response.status != 200:
    print('Error while searching')

tweets = json.loads(content.decode('utf-8'))
# convert json to a python dictionary

for tweet in tweets['statuses']:
        print(tweet['text'])

