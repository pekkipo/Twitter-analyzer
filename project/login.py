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

# Info
# dict([('hi', '123'), ('hey', '456')])
# dict is run on the list of tuples in a format key-value into a dictionary, which is handy

