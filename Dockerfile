# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
#FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install python3-pip -y
#RUN apt-get install gunicorn3 -y
COPY requirements.txt requirements.txt
COPY . /opt/
RUN pip3 install -r requirements.txt
WORKDIR /opt/
#CMD ["gunicorn3", "-b", "0.0.0.0:5001", "app: app", "--workers=5"]
#CMD ["gunicorn", "-b", "0.0.0.0:3001", "app:app", "--workers=5"]
# CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "1", "--worker-class", "eventlet", "manage:manage"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:3000"]