# allowing to interact with the DB
from psycopg2 import pool

class Database:
        __connection_pool = None

        @classmethod
        def initialize(cls, **kwargs): # not __init__ method!
            cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                              10,
                                                              **kwargs
                                                              )

        @classmethod
        def get_connection(cls):
            return cls.__connection_pool.getconn()

        @classmethod
        def return_connection(cls, connection):
            # in this case we need the reference to connection that we want to put back in
            Database.__connection_pool.putconn(connection)


        @classmethod
        def close_all_connections(cls):
            Database.__connection_pool.closeall()


class CursorFromConnectionPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # enter method is the beginning of the with statement
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):

        # deal with the error. If it occurs - roll back the connection
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit() # DON'T forget! Commit then close
            # here we should be returning the connections
            Database.return_connection(self.connection)
