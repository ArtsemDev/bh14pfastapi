FROM python:3.11.7-alpine3.19

ARG APP_PATH=/opt
ARG UNAME=www
ARG UID=1000

WORKDIR $APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1


COPY . $APP_PATH

RUN apk add build-base && \
    pip install --no-cache-dir --upgrade -r $APP_PATH/migrations/requirements.txt && \
    adduser -u $UID -s /bin/bash -D -S $UNAME
USER $UNAME