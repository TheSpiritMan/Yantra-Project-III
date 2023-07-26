FROM python:3.11.4-alpine3.18 AS base
WORKDIR /app
RUN apk add --update make automake gcc g++ subversion python3-dev qt5-qtbase-dev gfortran
# RUN pip install virtualenv
# RUN virtualenv venv && source venv/bin/activate
COPY requirements.txt ./
RUN pip install -r requirements.txt