FROM python:3.11.7-slim

ARG APP_PATH=/opt

WORKDIR $APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1


COPY ./blog $APP_PATH/blog
COPY ./src $APP_PATH/src

RUN pip install --no-cache-dir --upgrade -r $APP_PATH/blog/requirements.txt