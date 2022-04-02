FROM python:3.10

RUN pip install pipenv

ENV PROJECT_DIR /usr/local/src/webapp


COPY . code
WORKDIR /code


COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy