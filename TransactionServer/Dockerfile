FROM python:3.10

RUN pip install pipenv

ENV PROJECT_DIR /usr/local/src/webapp
ENV ENVIRONMENT "production"
ENV DB_CONNECTION_STRING "mongodb://dta:8npqgJ1Pqo1PlO5ZYDeS8GARIP0gMkvgEKCNT2SrmhyzIv1jNJghm7glfbscMyivGnKXltGijeJMkX5Jg2qajQ==@dta.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dta@"
ENV DB_CONNECTION_TYPE "CONNECTION_STRING"
ENV DB_NAME "dta"
ENV SECRET_KEY "d0946e53d85e7a611ba84f813b7c8ee7269d1c2cbf5dec78a1d3636c25851865d5eed5b99d96fefe6da6f456c281f52ba11040cf921bdd1a281f94a9973bda77"
ENV DEBUG "True"
ENV LOG "True"
ENV HARD_CODE_USER "False"


COPY . code
WORKDIR /code


COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy