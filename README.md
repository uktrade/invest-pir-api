# PIR-API

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]

## Requirements

[Python >= 3.5.5](https://www.python.org/downloads/release/python-360/)

[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)


## Local installation

    $ git clone https://github.com/uktrade/pir-api
    $ cd pir-api
    $ make

## Running with Docker
Requires all host environment variables to be set.

    $ make docker_run

### Run debug webserver in Docker

    $ make docker_debug

### Run tests in Docker

    $ make docker_test

### Host environment variables for docker-compose
``.env`` files will be automatically created (with ``env_writer.py`` based on ``env.json``) by ``make docker_test``, based on host environment variables with ``PIR_API`` prefix.

## Debugging

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## CSS development

### Requirements
[node](https://nodejs.org/en/download/)
[SASS](http://sass-lang.com/)

	$ npm install
	$ npm run sass-dev

### Update CSS under version control

	$ npm run sass-prod

### Rebuild the CSS files when the scss file changes

	$ npm run sass-watch


[circle-ci-image]: https://circleci.com/gh/uktrade/pir-api/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/pir-api/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/pir-api/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/pir-api

