FROM python:3.11.7-slim

ARG APP_PATH=/opt
ARG UNAME=www
ARG UID=1000

WORKDIR $APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1


COPY . $APP_PATH

RUN pip install --no-cache-dir --upgrade -r $APP_PATH/migrations/requirements.txt
