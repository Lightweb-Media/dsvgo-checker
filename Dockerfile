FROM alpine:latest
RUN apk update && apk add bind-tools
RUN apk add --no-cache gcc libc-dev linux-headers
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 

ARG USER=app
ENV HOME /home/$USER

# install sudo as root
RUN apk add --update sudo

# add new user
RUN adduser -D $USER \
        && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
        && chmod 0440 /etc/sudoers.d/$USER

USER $USER
RUN pip3 install --upgrade pip
RUN pip3 install uwsgi

WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
CMD [ "uwsgi", "--ini", "uwsgi.ini"]