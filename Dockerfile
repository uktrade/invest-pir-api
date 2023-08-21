FROM python:3.9.2

### 1. Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DOCKERIZE_VERSION v0.6.1

### 2. Setup GDAL
RUN apt-get update &&\
    apt-get install -y gettext redis-server libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev && apt-get clean curl && rm -rf /var/lib/apt/lists/*


### 3. Add dockerize to allow waiting for the DB to load.
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

### 4. Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./fonts/* /usr/share/fonts/
RUN fc-cache -f -v

ADD requirements_test.txt /usr/src/app/

### 5. Install packages
RUN set -e; \
    /usr/local/bin/python -m pip install --upgrade pip ;\
    python -m pip install pip-tools ;\
    python -m pip install --no-cache-dir -r requirements_test.txt --src /usr/local/src ;

ADD . /usr/src/app

### 6. Expose port
EXPOSE 8003
