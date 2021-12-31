FROM python:3.8.2-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc libgdal-dev  -y
RUN mkdir /app
WORKDIR /app
COPY ./etc/docker/web/requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
