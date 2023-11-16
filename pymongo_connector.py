# IMPORTS

import pymongo



# CONSTANTS

USER = 'root'
PASSWORD = 'password'
HOST = '127.0.0.1'
PORT = '27017'
DBNAME = 'bookmanager'
COLLECTION = 'Book'



# MAIN

client = pymongo.MongoClient(f'mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/')
db = client[DBNAME]
collection = db[COLLECTION]


