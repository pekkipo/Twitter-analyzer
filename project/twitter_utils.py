import oauth2
import constants
import urllib.parse as urlparse # as just renames it

# Create consumer to identify the app
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
# will kinda global reusable variable

def get_request_token():
    # create a client to perform a request for the request token
    client = oauth2.Client(consumer)
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    # left - what the request returns
    # first request
    # refer to the order in the course
    if response.status != 200:  # 200 is everything's fine
        print("An error occured when getting the request token from Twitter")

    # Get the request token parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))
    # content is in a format of query string parameter
    # we convert it into a dictionary
    # decode converts bytes to strings
    # this is indeed more readable then the ori


def get_oauth_verifier(request_token):
    # Ask the user
    # We are doing Pin auth. Just for learning purpose. We have a console application
    print("Go to the following web-site:")

    print(get_oauth_verifier_url(request_token))
    # User must type the pin

    return input("What is the pin? ")


def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])


def get_access_token(request_token, oauth_verifier):

    # Create a token object which contains the request token and the verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    client = oauth2.Client(consumer, token)

    # We use this client to get an access token
    # Ask Twitter for a request token and Twitter knows it should give us it because we verified the request token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

