# syntax=docker/dockerfile:1
FROM python:3.9

WORKDIR /mangalibrary 

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY run.py config.py db_create.py worker.py boot.sh ./
RUN chmod +x boot.sh 

EXPOSE 5000
