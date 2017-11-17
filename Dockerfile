FROM python:3.6.0

RUN wget http://rubies.travis-ci.org/ubuntu/14.04/x86_64/ruby-2.3.1.tar.bz2 \
    && tar xvjf ruby-2.3.1.tar.bz2 \
    && cp -rp ruby-2.3.1/* /usr/local/ \
    && rm -rf ruby-2.3.1.tar.bz2 ruby-2.3.1/

RUN mkdir /code
WORKDIR /code

RUN easy_install -U pip
RUN pip install -U pip setuptools

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
