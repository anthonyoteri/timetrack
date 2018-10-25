FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN pip install --upgrade pip

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
