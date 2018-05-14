FROM python:3.6


# Current version of debian in the python image is waaayyy tooo ollllddddd.
# Need libcairo2 > 1.4
# gettext to compile translations
# redis for caching and sessions
RUN sed '1 s/jessie/buster/' /etc/apt/sources.list > /etc/apt/sources.list.temp
RUN mv /etc/apt/sources.list.temp /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y gettext redis-server libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev && apt-get clean && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./fonts/* /usr/share/fonts/
RUN fc-cache -f -v

COPY . /usr/src/app

COPY requirements.txt /usr/src/app/
# Different src directory for pip to prevent 'pip install -e' packages to be installed in /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src


RUN echo $HOME

CMD ["/usr/src/app/docker/cmd-webserver.sh"]

EXPOSE 8000
