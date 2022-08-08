# base image
FROM python:3.8

RUN apt-get update && apt-get install curl gnupg -y \
  && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install google-chrome-stable -y --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y uwsgi && \    
    apt-get install -y  dnsutils && \
    apt-get install -y  redis-server && \
    apt-get install -y uwsgi-plugin-python3


RUN export PYTHON=python3.8
#RUN uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python38"
    # set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
#RUN pip install uwsgi
# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN useradd -ms /bin/bash app
USER app
RUN python3 -m pip install -r requirements.txt

# copy project
COPY . /usr/src/app
COPY uwsgi.ini /etc/uwsgi/apps-enabled/

