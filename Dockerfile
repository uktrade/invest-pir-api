FROM python:3.9


# Current version of debian in the python image is waaayyy tooo ollllddddd.
# Need libcairo2 > 1.4
# gettext to compile translations
# redis for caching and sessions
RUN apt-get update

RUN apt-get install -y gettext redis-server libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev && apt-get clean curl && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./fonts/* /usr/share/fonts/
RUN fc-cache -f -v

ADD requirements.txt /usr/src/app/

# Because directory-signature-auth uses pip internals
RUN pip install --upgrade pip
# Different src directory for pip to prevent 'pip install -e' packages to be installed in /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

ADD . /usr/src/app

# Install dockerize https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget -q https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

CMD ["/usr/src/app/docker/cmd-webserver.sh"]
