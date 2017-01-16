import constants
import oauth2
import urllib.parse as urlparse # as just renames it

# identify the app
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

# create a client
client = oauth2.Client(consumer)

response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
# left - what the request returns
# first request
# refer to the order in the course
if response.status != 200: # 200 is everything's fine
    print("An error occured when getting the request token from Twitter")


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


# We are doing Pin auth. Just for learning purpose. We have a console application
print("Go to the following web-site:")
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))
# {} will be replaced by two variables
# request_token is a dictionary
# user gets the pin from the web-page

# User must type the pin
oauth_verifier = input("What is the pin? ")

token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)

client = oauth2.Client(consumer, token)

# We use this client to get an access token
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token  = dict(urlparse.parse_qsl(content.decode('utf-8')))

print(access_token)

# Info
# dict([('hi', '123'), ('hey', '456')])
# dict is run on the list of tuples in a format key-value into a dictionary, which is handy

