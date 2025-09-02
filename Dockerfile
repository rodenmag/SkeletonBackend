FROM python:3.8-slim
ENV PYTHONNUNBUFFERED 1

RUN apt-get update
RUN apt-get install sudo
RUN apt-get install -y default-jre
RUN apt-get install -y redis-server

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
