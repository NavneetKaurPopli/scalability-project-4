from sys import stdout
from django.shortcuts import render
from django.http import HttpResponse
from api.utils.quoteServer import getQuote
from api.utils.user import *
from api.utils.errors import handleViewError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.utils.decorators import logRequest, auth
from api.utils.db import mongoZip
import json 
from rest_framework import status

@csrf_exempt
@api_view(['POST'])
def login_user(request, **kwargs):
    print("in login")
    username = request.data['username']
    password = request.data['password']
    status = login(username=username, password=password)
    print("status is, ", status)
    return Response("request", status=status)

#@auth
@logRequest
@api_view(['GET'])
def quote(request, **kwargs):
    username = request.GET.get('username')
    user = getUser(username, mongoZip(['username', 'balance']))
    # TODO: redis this, then have the buy and sell commands use the redis cache before hitting the quote server
    ticker = kwargs.get('ticker')
    if ticker is None:
        ticker = request.GET.get('ticker')
    try:
        if ticker is None:
            raise Exception('No ticker specified')
    
        
        return Response(getQuote(ticker, user,request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST', 'PATCH'])
def add(request):
     
    
    username = request.data.get('username')
    user = getUser(username, mongoZip(['username', 'balance']))
    amount = request.data.get('amount', False) 
    
    try:
        return Response(addBalance(user, amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt               
@logRequest
@api_view(['POST'])
def buy(request):
    username = request.data.get('username')
    user = getUser(username, mongoZip(['username', 'balance']))
    ticker = request.data.get('ticker', False)
    amount = request.data.get('amount', False)
    # print(ticker, amount, username)
    try: 
        if ticker == False: 
            raise Exception('No ticker specified')
        if amount == False:
            raise Exception('No amount specified')
    
        return Response(buyStock(user, amount,getQuote(ticker,user, request.transactionId), request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST','PATCH'])
def commit_buy(request):
    
    username = request.data.get('username')
    user = getUser(username, mongoZip(['username', 'balance', 'pending_buy', 'stocks']))
    try:
        return Response(commitBuy(user, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)
         
#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_buy(request): 
    username = request.data.get('username')
    user = getUser(username, mongoZip(['username', 'balance', 'pending_buy']))
    try:
        return Response(cancelBuy(user, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def sell(request):
    username = request.data.get('username')
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    user = getUser(username, mongoZip(['username', 'balance', 'stocks']))
    try:
        return Response(sellStock(user, amount, getQuote(ticker, user, request.transactionId), request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def commit_sell(request):
    username = request.data.get('username')
    user = getUser(username, mongoZip(['username', 'balance', 'pending_sell', 'stocks']))
    try:
        return Response(commitSell(user, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_sell(request):
    username = request.data.get('username')
    user = getUser(username, mongoZip(['username', 'balance', 'pending_sell']))
    try:
        return Response(cancelSell(user, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def set_buy_amount(request): 
    username = request.data.get('username')
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    user = getUser(username, mongoZip(['username', 'balance']))
    try:
        return Response(setBuyAmount(user, ticker,amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_set_buy(request):
    username = request.data.get('username')
    ticker = request.data.get('ticker', False)
    user = getUser(username, mongoZip(['username', 'balance', 'buy_triggers']))
    try:
        return Response(cancelBuyTrigger(user,ticker,request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def set_buy_trigger(request):
    username = request.data.get('username')
    ticker = request.data.get('ticker', False)
    price = request.data.get('price', False)
    user = getUser(username, mongoZip(['username', 'balance', 'pending_trigger']))
    try:
        return Response(setBuyTrigger(user, ticker, price,request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def set_sell_amount(request):
    username = request.data.get('username')
    amount = request.data.get('amount', False)
    ticker = request.data.get('ticker', False)
    user = getUser(username, mongoZip(['username', 'balance']))
    try:
        return Response(setSellAmount(user, ticker, amount, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def set_sell_trigger(request):
    username =  request.data.get('username')
    price = request.data.get('price', False)
    ticker = request.data.get('ticker', False)
    user = getUser(username, mongoZip(['username', 'balance', 'pending_trigger', 'stocks']))
    try:
        return Response(setSellTrigger(user, ticker, price, request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@csrf_exempt
@logRequest
@api_view(['POST'])
def cancel_set_sell(request):
    username = request.data.get('username')
    ticker = request.data.get('ticker', False)
    user = getUser(username, mongoZip(['username', 'balance', 'sell_triggers']))
    try:
        return Response(cancelSellTrigger(user, ticker,request.transactionId))
    except Exception as e:
        return handleViewError(e, request, user)

#@auth
@logRequest
@api_view(['GET'])
def dumplog(request):
    user = getUser(request.GET.get('username')) if 'username' in request.GET.keys() else None
    try:
        if 'username' in request.GET.keys():
            return Response(dumplogXML(request.GET['username']))
        return Response(dumplogXML())
    except Exception as e:
        return handleViewError(e, request, user)
    
#@auth
@logRequest
@api_view(['GET'])
def displaySummary(request):  
    username = request.GET.get('username')
    user = getUser(username)
    try:
        return Response(displayUserSummary(user))
    except Exception as e:
        return handleViewError(e, request, user)
    
#@auth
@csrf_exempt
@api_view(['POST'])
def createNewUser(request):
        print("#######################################################request is: ", request.data)
        body = request.data
        username = body.get('username')
        print("username is: ", username)
        password = body['password']
        name = body['name']
        
        if(createUser(name, username, password)):
            # TODO: log the user in when the account is created
            return Response("User created")
        
    # except Exception as e:
        
    #    return Response(e)

#@auth
@api_view(['GET'])
def getUserObj(request):
    try:

        user = getUser("test")
        print(user)
        return Response(user)
    except Exception as e:
        return handleViewError(e, request)