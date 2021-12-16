FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY . .
RUN set -ex \
    && buildDeps=' \
        python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        python3-pip \
        python3-requests \
        default-mysql-client \
        default-mysql-server \
        default-libmysqlclient-dev \
        apt-utils
RUN /usr/local/bin/python -m pip install --upgrade pip
#RUN ["source", "activate"]
RUN pip3 install -r requirements.txt
RUN service mysql start

EXPOSE 8080
EXPOSE 8088
#RUN ["source", "activate"]

#CMD python manage.py runserver 8080