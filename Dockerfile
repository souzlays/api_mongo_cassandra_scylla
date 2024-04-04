FROM python:3.6 as dev

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt