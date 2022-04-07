from api.utils.db import getDb, dbCallWrapper
from api.utils.errors import handleViewError
from datetime import datetime
from os import path
import time
import environ
from bson.objectid import ObjectId

# initialize the environment
env = environ.Env()
env.read_env()





db, client = getDb()
def logRequest(view):
    """   
    Logs the command sent to the API.
    to the database log collection
    catches all exceptions and logs them
    """ 
    def wrapper(request, **kwargs):
        log = env('LOG') == 'True' or env('LOG') == True
        if(not log):
            print("NO LOG")
            return view(request, **kwargs)

        timestamp = str(int(time.time()*1000))	
        # Get the command name
        command = request.path.split('/')[-2]	
        # Get the parameters	
        # Create the JSON
        json = {
        	'type': 'userCommand',
        	'timestamp': timestamp,
        	'command': command.upper(),
        	'server': 'transactionserver',
        }
        
        if request.method == 'POST' :

            allParams = request.POST.dict()
            request.data = allParams
        else:
            allParams = request.GET.dict()
        
        
        json['username'] = allParams['username'] if 'username' in allParams.keys() else 'admin' 
        if 'ticker' in allParams.keys():
            json['stockSymbol'] = allParams['ticker']
        objId = dbCallWrapper(json, func = db.log.insert_one)
        request.transactionId = str(int(ObjectId(objId).binary.hex(), 16)) # cast to int
        print("log")
        return view(request, **kwargs)
        
    return wrapper

def auth(view):
    """
    Authenticates the user.
    """
    def wrapper(request, **kwargs):
        if request.headers.get('Authorization') == env('SECRET_KEY') or env('ENVIRONMENT') == 'development':
            return view(request, **kwargs)
        else:
            return handleViewError(Exception('Unauthorized'), request, 401)
    return wrapper