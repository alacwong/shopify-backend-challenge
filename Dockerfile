FROM python:3.7-slim

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn","--workers=2", "wsgi:application", "-b", "0.0.0.0:5000"]
