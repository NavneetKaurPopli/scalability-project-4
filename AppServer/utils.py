from pymongo import MongoClient
def get_db_handle(db_name,host, port ):

    client = MongoClient(host=host,
                      port=int(port)
                     )
    db = client[db_name]
    return db, client

def get_db_handle_connection_string(connection_string):
    print("made it here")
    client = MongoClient(connection_string)
    # db = client[db_name]
    return client