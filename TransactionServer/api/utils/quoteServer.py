import socket
from api.utils.db import *
import datetime
import random
import redis
import json
import os
class QuoteNotAvailableError(Exception):
    pass

db, client = getDb()
def make_fake_quote(ticker, user):
    pass

def getQuote(ticker, user, request):
    
        starttime = datetime.datetime.now()
        HOST = '192.168.4.2'
        PORT = 4444
       
        r = redis.Redis(host='localhost', port=6379, db=0)

        if r.exists(ticker):
            quote = json.loads(r.get(ticker))
            logJsonObject({
                # SYSTEM EVENT LOG FOR CACHE
                'username': user['username'],
                'timestamp': int(round(datetime.datetime.now().timestamp() * 1000)),
                'server': 'transactionserver: ' + socket.gethostname(),
                'type': 'debugEvent',
                'debugMessage': 'Cache Hit for ' + ticker,
                'command': 'QUOTE',
                'stockSymbol': ticker,
            })
            return {
                'ticker': ticker,
                'user': user['username'],
                'timestamp': quote['timestamp'],
                'price': quote['price'],
                'cryptokey': quote['cryptokey'],
            }
        else:
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                try:
                    sock.connect((HOST, PORT))
                    sock.sendall(ticker.encode()+ b' ' + user['username'].encode() + b'\n')
                    data = sock.recv(1024)
                    decodedData = data.decode().split(',')
                    logJsonObject({
                        # QUOTE SERVER LOG 
                        'stockSymbol': ticker,
                        'price': decodedData[0],
                        'username': user['username'],
                        'quoteServerTime': (datetime.datetime.now() - starttime).total_seconds(),
                        'timestamp': int(round(datetime.datetime.now().timestamp() * 1000)),
                        'cryptokey': decodedData[3],
                        'server': 'transactionserver: ' + socket.gethostname(),
                        'type': 'quoteServer',
                    })

                    r.set(ticker, json.dumps({
                        'timestamp': int(round(datetime.datetime.now().timestamp() * 1000)),
                        'price': decodedData[0],
                        'cryptokey': decodedData[3],
                    }), ex=60)

                    return {
                        'ticker': ticker,
                        'price': decodedData[0],
                        'username': user['username'],
                        'timestamp': decodedData[2],
                        'cryptographicKey': decodedData[3]
                    }
                except socket.error as err:
                    raise QuoteNotAvailableError('Error connecting to server: {}'.format(err))

        





