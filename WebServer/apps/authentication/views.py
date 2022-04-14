from pickle import TRUE
from sys import excepthook
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from .utils.decorators import *
from rest_framework.decorators import api_view
from .renderers import JSONRenderer

import environ
from rest_framework import status
import requests
from .utils.jwt_token import *
import json



env = environ.Env()
environ.Env.read_env()

ts_secret = env('TRANSACTION_SERVER_SECRET_ID')
ts_header = {'Content-type':'application/json', 'Accept':'application/json'}
ts_uri = env('TRANSACTION_SERVER_URI')
ts_port = env('TRANSACTION_SERVER_PORT')


@csrf_exempt
@api_view(['POST'])
# @permission_required([AllowAny])
def register(request, **kwargs):

    name = request.data['name']
    username = request.data['username']
    token = generate_jwt_token(username)
    password = request.data['password']
    data={'name':name, 'username': username, 'password': password}
    r = requests.post('http://127.0.0.1:8002/api/create_user/', data=json.dumps(data), headers=ts_header)
    
    if r.status_code  == '400':
        return Response("bad request", status=status.HTTP_400_BAD_REQUEST)
    return  Response({"access_token":str(token)}, status=status.HTTP_200_OK)
   

@csrf_exempt
@api_view(['POST'])
def login(request, **kwargs):

    username = request.data['username']
    password = request.data['password']
    data={'username': username, 'password': password}
    r = requests.post(ts_uri + ts_port +':/api/login_user/', data=json.dumps(data), headers=ts_header)
    if r.status_code == 200:
        token = generate_jwt_token(username)
        return  Response({"access_token":str(token)}, status=status.HTTP_200_OK)
    return Response("bad request", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def add(request, **kwargs):
    username = request.data['username']
    amount = request.data['amount']
    data = {"username": username, "amount": amount}
    r = requests.post(ts_uri + ':' + ts_port + '/api/add/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@auth
def quote(request, **kwargs):
    pass

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def buy(request):
    username = request.data['username']
    amount = request.data['amount']
    ticker = request.data['ticker']
    data = {"username": username, "amount": amount, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/buy/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def commit_buy(request):
    username = request.data['username']
    data = {'username': username}
    r = requests.post(ts_uri + ':' + ts_port + '/api/commit_buy/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)   

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def cancel_buy(request):
    username = request.data['username']
    data = {'username': username}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/cancel_buy/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def sell(request):
    username = request.data['username']
    amount = request.data['amount']
    ticker = request.data['ticker']
    data = {"username": username, "amount": amount, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port + '/api/sell/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def commit_sell(request):
    username = request.data['username']
    data = {'username': username}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/commit_sell/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)   

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def cancel_sell(request):
    username = request.data['username']
    data = {'username': username}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/cancel_sell/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)   

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def set_buy_amount(request):
    username = request.data['username']
    amount = request.data['amount']
    ticker = request.data['ticker']
    data = {"username": username, "amount": amount, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/set_buy_amount/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def cancel_set_buy(request):
    username = request.data['username']
    ticker = request.data['ticker']
    data = {"username": username, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/cancel_set_buy/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def set_buy_trigger(request):
    username = request.data['username']
    amount = request.data['amount']
    ticker = request.data['ticker']
    data = {"username": username, "amount": amount, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/set_buy_trigger/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def set_sell_amount(request):
    username = request.data['username']
    amount = request.data['amount']
    ticker = request.data['ticker']
    data = {"username": username, "amount": amount, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/set_sell_amount/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def set_sell_trigger(request):
    username = request.data['username']
    amount = request.data['amount']
    ticker = request.data['ticker']
    data = {"username": username, "amount": amount, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/set_sell_trigger/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@auth
def cancel_set_sell(request):
    username = request.data['username']
    ticker = request.data['ticker']
    data = {"username": username, "ticker": ticker}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/cancel_set_sell/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@auth
def dumplog(request):
    username = request.GET['username']
    data = {"username": username}
    r = requests.get(ts_uri + ':' + ts_port +  '/api/dumplog/', params=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@auth
def display_summary(request):
    username = request.data['username']
    data = {"username": username}
    r = requests.post(ts_uri + ':' + ts_port +  '/api/display_summary/', data=json.dumps(data), headers=ts_header)
    return Response(r.text, status=r.status_code)
