FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

ADD requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && apk add postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

ADD . /code/
WORKDIR /code

RUN python manage.py collectstatic --no-input

EXPOSE 8000
