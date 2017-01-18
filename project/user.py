from database import CursorFromConnectionPool
# database is database.py file, connect is the method
import oauth2
from twitter_utils import consumer
import json
import constants
import urllib.parse as urlparse # as just renames it

class User:

    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.email)

    def save_to_db(self):
        with CursorFromConnectionPool() as cursor:
                 cursor.execute('INSERT INTO users(email,first_name,last_name, oauth_token, oauth_token_secret) VALUES (%s,%s,%s,%s,%s)',
                                   (self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_token_secret))

    @classmethod
    def load_from_db_by_email(cls, email): # cls - currently bound class. self woult be currently bound object
        # note that we must pass the email as a parameter
        with CursorFromConnectionPool() as cursor:
                cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
                user_data = cursor.fetchone()
                if user_data: # if not None
                    return cls(email=user_data[1],
                           first_name=user_data[2],
                           last_name=user_data[3],
                           oauth_token = user_data[4],
                           oauth_token_secret = user_data[5],
                           id=user_data[0])
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

