from python:3

RUN apt update

WORKDIR /app

RUN pip install openai flask flask-cors


CMD python server.py