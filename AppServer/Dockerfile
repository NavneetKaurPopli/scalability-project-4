# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PROJECT_DIR /usr/local/src/serverapp
RUN pip install pipenv

EXPOSE 8000
ENV LISTEN_PORT=8000
ENV UWSGI_INIT uwsgi.ini

WORKDIR ${PROJECT_DIR}/
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . ${PROJECT_DIR}/

