FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./fonts/* /usr/share/fonts/
RUN fc-cache -f -v

COPY . /usr/src/app

COPY requirements.txt /usr/src/app/
# Different src directory for pip to prevent 'pip install -e' packages to be installed in /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

# gettext to compile translations
# redis for caching and sessions
RUN apt-get update && apt-get install -y gettext redis-server libpango1.0-dev && apt-get clean && rm -rf /var/lib/apt/lists/*


RUN echo $HOME

CMD ["/usr/src/app/docker/cmd-webserver.sh"]

EXPOSE 8000
