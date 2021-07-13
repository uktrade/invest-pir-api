# invest-pir-api

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

**Personalised investment report API - the Department for International Trade (DIT)**


## Development

### Installing installation

    $ git clone https://github.com/uktrade/invest-pir-api
    $ cd invest-pir-api
    $ virtualenv .venv -p python3.6
    $ source .venv/bin/activate
    $ pip install -r requirements_test.txt
    # Start postgres now before proceeding.
    $ make debug_db
    $ make debug_migrate
    $ make debug_createsuperuser

### Requirements

[Python 3.6](https://www.python.org/downloads/release/python-360/)
[Postgres 9.5](https://www.postgresql.org/)
[Redis server](https://redis.io/)
[Cairo](https://www.cairographics.org/download/)
[Pango](https://www.pango.org/HelpOnInstalling/BasicInstallation)
[GNU Gettext](https://www.gnu.org/software/gettext/)

---

### Configuration

### Run debug tests

    $ make debug_test


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


#### AWS envars

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


## CSS development

We use SASS CSS pre-compiler. If you're doing front-end work your local machine will also need the following dependencies:

[node](https://nodejs.org/en/download/)
[SASS](https://rubygems.org/gems/sass/versions/3.4.22)

Then run:

    $ npm install

We add compiled CSS files to version control. This will sometimes result in conflicts if multiple developers are working on the same SASS files. However, by adding the compiled CSS to version control we avoid having to install node, npm, node-sass, etc to non-development machines.

You should not edit CSS files directly, instead edit their SCSS counterparts.

### Update CSS under version control

    $ make compile_css



## Helpful links
* [GDS service standards](https://www.gov.uk/service-manual/service-standard)
* [GDS design principles](https://www.gov.uk/design-principles)

## Related projects:
https://github.com/uktrade?q=directory
https://github.com/uktrade?q=great

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-cms/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/invest-pir-api/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/invest-pir-api/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/invest-pir-api

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
