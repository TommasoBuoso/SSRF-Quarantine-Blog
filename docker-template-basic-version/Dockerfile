FROM ubuntu:18.04
ENV BOT_URL=https://example.seclab.dais.unive.it

########################################################################
# Requirements
RUN apt-get update \
 && apt-get install -y uwsgi python3 python3-venv uwsgi-plugin-python3 sqlite3 \ 
         supervisor \
         libfontconfig libcap2-bin ssl-cert socat firefox curl \
 # allow uwsgi to bind to *:80 \
 && setcap cap_net_bind_service=+ep /usr/bin/uwsgi-core

########################################################################
# Website
# create the example user and copy the app in its home directory
USER root
RUN useradd -U -m -s /bin/bash example
COPY ./app /home/example/app
RUN mkdir -p /home/example/instance && chown -R example:example /home/example
USER example
# Install app requirements in a python virtualenv
RUN mkdir /home/example/.venvs \
 && python3 -m venv /home/example/.venvs/example \
 && . /home/example/.venvs/example/bin/activate \
 && pip install -r /home/example/app/requirements.txt

########################################################################
# Entrypoint
COPY supervisor.conf /
USER root 
EXPOSE 80
# run app
CMD supervisord -c /supervisor.conf
