#official base image
FROM python:3.8-alpine

# set environment variables
WORKDIR /usr/src/app

# set environnment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip uninstall PIL
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . /usr/src/app
