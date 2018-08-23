# PIR-API

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]

## Requirements

[Python >= 3.5.5](https://www.python.org/downloads/release/python-360/)

[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)


## Local installation

    $ git clone https://github.com/uktrade/invest-pir-api
    $ cd invest-pir-api
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


[circle-ci-image]: https://circleci.com/gh/uktrade/invest-pir-api/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/invest-pir-api/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/invest-pir-api/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/invest-pir-api


### Environment Variables

#### RESTRICT_ADMIN 

Default: True.

Restrict admin to particular IP addresses


#### ALLOWED_ADMIN_IPS/ALLOWED_ADMIN_IP_RANGES

Default: []

Restrict to these IP addresses

#### REDIS_URL

Default: None

#### LOGIN_FAILURE_LIMIT

Default: 10 

How many times a user can fail their password before the "please contact
an admin" screen appears

#### LOGIN_FAILURE_COOLOFF

Default: 24 (hours)

How long until a user at an IP address can retry

#### RESET_EMAIL

Default: None

When a user enters their password more than allowed. They are presented with a
screen asking an admin to unlock their account again. They enter their email,
and an admin is emailed. The RESET_EMAIL is said admin's email.


##### DEFAULT_FROM_EMAIL

Default: None


##### MODERATION_MODERATORS

Default: None

Tuple of moderators’ email addresses to which notifications will be sent.


#### SIGNATURE_SECRET

Default: abc

Hawk authentication key

#### GOV_NOTIFY_API_KEY

Credentials for the gov email service

#### EMAIL_UUID

ID of email with report.

#### DEFAULT_EMAIL_UUID

ID of email with *default report*.


#### FRONTEND_URL

Where the corresponding URL for the frontend is.

----

### AWS envars

Static and media files

 - AWS_STORAGE_BUCKET_NAME
 - AWS_ACCESS_KEY_ID
 - AWS_SECRET_ACCESS_KEY
 - AWS_DEFAULT_REGION

Only for PDFs

  - AWS_S3_PDF_STORE_ACCESS_KEY_ID
  - AWS_S3_PDF_STORE_SECRET_ACCESS_KEY
  - AWS_S3_PDF_STORE_BUCKET_NAME
  - AWS_S3_PDF_STORE_BUCKET_REGION
