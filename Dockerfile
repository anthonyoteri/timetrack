FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --no-input

EXPOSE 8000
