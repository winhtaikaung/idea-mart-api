FROM python:3.6.4
MAINTAINER winhtaikaung(winhtaikaung28@hotmail.com)

RUN mkdir /app
WORKDIR  /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 5000