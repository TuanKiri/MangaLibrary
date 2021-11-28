# syntax=docker/dockerfile:1
FROM ubuntu:20.04

WORKDIR /home/mangalibrary

RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP run.py

COPY app app
COPY run.py config.py db_create.py ./
RUN python3 db_create.py

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
