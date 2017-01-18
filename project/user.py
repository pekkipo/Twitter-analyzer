from database import CursorFromConnectionPool
# database is database.py file, connect is the method
import oauth2
from twitter_utils import consumer
import json
import constants
import urllib.parse as urlparse # as just renames it

class User:

    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.screen_name)

    def save_to_db(self):
        with CursorFromConnectionPool() as cursor:
                 cursor.execute('INSERT INTO users(screen_name, oauth_token, oauth_token_secret) VALUES (%s,%s,%s)',
                                   (self.screen_name, self.oauth_token, self.oauth_token_secret))

    @classmethod
    def load_from_db_by_screen_name(cls, screen_name): # cls - currently bound class. self woult be currently bound object
        # note that we must pass the email as a parameter
        with CursorFromConnectionPool() as cursor:
                cursor.execute('SELECT * FROM users WHERE email=%s', (screen_name,))
                user_data = cursor.fetchone()
                if user_data: # if not None
                    return cls(screen_name = user_data[1],
                           oauth_token = user_data[3],
                           oauth_token_secret = user_data[4],
                           id=user_data[0])
                    # order on user_data array corresponds to that of the columns in a Postgre table
                #else:
                   # return None # redundant as by default func returns None


    # perform a request
    def twitter_request(self, url, verb='GET'): # Verbs like GET, POST etc

        # GET is a default value and will be used if nothing were passed as a verb

        # Create an authenticated Token object and use it to perform Twitter API calls on behalf of the user
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)
        # Make Twitter API calls
        response, content = authorized_client.request(url, verb)
        if response.status != 200:
           print('Error while searching')

        return json.loads(content.encode('utf-8'))
        # convert json to a python dictionary

