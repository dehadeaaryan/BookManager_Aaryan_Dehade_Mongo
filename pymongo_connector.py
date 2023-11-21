# IMPORTS

from pymongo import MongoClient



# CONSTANTS

USER = 'root'
PASSWORD = 'password'
HOST = '127.0.0.1'
PORT = '27017'
DBNAME = 'bookmanager'
PUBLISHER_COLLECTION = 'Publisher'
BOOK_COLLECTION = 'Book'



# CONNECTION CLASS

class DBConnection:
    """Class that represents a database connection."""
    def __init__(self, user: str = USER, password: str = PASSWORD, host: str = HOST, port: str = PORT, dbname: str = DBNAME, publisherCollection: str = PUBLISHER_COLLECTION, bookCollection: str = BOOK_COLLECTION):
        """Constructor method."""
        # connect to the database
        self.client = MongoClient(f'mongodb://{user}:{password}@{host}')
        self.db = self.client[dbname]
        self.publisher_collection = self.db[publisherCollection]
        self.book_collection = self.db[bookCollection]

    def getClient(self):
        """Method that returns the client."""
        return self.client
    
    def getDB(self):
        """Method that returns the database."""
        return self.db

    def getPublisherCollection(self):
        """Method that returns the collection."""
        return self.publisher_collection
    
    def getBookCollection(self):
        """Method that returns the collection."""
        return self.book_collection
    
    def close(self):
        """Method that closes the connection to the database."""
        self.client.close()
