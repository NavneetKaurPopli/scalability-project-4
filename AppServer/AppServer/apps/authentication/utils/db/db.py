import environ
from ...utils import get_db_handle, get_db_handle_connection_string
from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from pymongo.cursor import Cursor
from pymongo import MongoClient


env = environ.Env()

environ.Env.read_env()

def getDb():
    print("made it here")
    client = MongoClient(env('DB_HOST_URI'))
    # db = client[db_name]
    return client
    
        
