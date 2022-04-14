# DTA

Our implementation of the Day Trading Application (DTA) uses two Django apps: Transaction Server and App Server. These projects are found in the TransactionServer and AppServer directories respectively.


## Transaction Server
The transaction server is built using Django. The root of the project can be found in TransactionServer/TransactionServer. This contain Django generated (modified by us) files, most importantly settings.py and urls.py. The settings file has various settings for the project and the urls.py file defines the URL patterns for the project. The urls.py includes an app called api at the /api/ endpoint. This app is used to interact with the transaction server. The transaction server takes in a request, if it has the @logRequest decorator, it logs the request to the database and assigns a transaction number to be used throughout the transaction. Finally the transaction server requires a .env file to be present. This is used to connect to a database and various settings as well. It needs values like DB_CONNECTION_STRING, DB_CONNECTION_TYPE, SECRET_KEY, DEBUG, LOG, HARD_CODED_USER, ENVIRONMENT and DJANGO_ALLOWED_HOSTS.

Some key files in the transaction server are: api/views.py, api/utils/user.py, api/utils/db.py. 

## WebServer

The web server is also built using Django and is mainly used to validate requests. It has a similar structure because of Django. Once the requests are validated it routes the request onto the transaction server

## Console App

The console app is used to run the workload files and can be found in the ConsoleApp directory. The main file is ThreadedDTA which takes a workload file and parses it into different users and assigns them a thread. 