FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install flask psycopg2-binary requests

COPY . .

CMD [ "python3", "main.py"]
