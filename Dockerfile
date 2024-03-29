FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD . /code/

RUN pip install --upgrade pip \
    pip install -r requirements.txt