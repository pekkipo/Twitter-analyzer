from database import CursorFromConnectionPool
# database is database.py file, connect is the method

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
    def twitter_request(self, url, verb, consumer): # Verbs like GET, POST etc
        # Create an authenticated Token object and use it to perform Twitter API calls on behalf of the user
        authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)
        # Make Twitter API calls
        response, content = authorized_client.request(
            'https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')
        if response.status != 200:
            print('Error while searching')