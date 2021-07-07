
build: docker_test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

INSTALL_REQUIREMENT:= pip install -r requirements_test.txt
UPGRADE_PIP := pip install --upgrade pip

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv,node_modules,src
PYTEST := pytest . --cov=. --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test:
	$(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py migrate --noinput && \
	python manage.py collectstatic --noinput && \
	python manage.py clear_cache && \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f docker-compose.yml -f docker-compose-test.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-test.yml pull
DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json ./docker/env.test.json

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_DEBUG_ENV_VARS := \
	export PIR_API_DEBUG=true; \
	export PIR_API_PORT=8014; \
	export PIR_API_REDIS_URL=redis://redis:6379; \
	export PIR_API_SECRET_KEY=secret; \
	export PIR_API_SESSION_COOKIE_SECURE=false; \
	export PIR_API_SECURE_HSTS_SECONDS=0; \
	export PIR_API_SECURE_SSL_REDIRECT=false; \
	export PIR_API_SITE_ID=1; \
	export PIR_API_TEST=true; \
	export PIR_API_DATABASE_URL=postgres://debug:debug@postgres:5432/invest_pir_api_debug; \
	export PIR_API_RECAPTCHA_PUBLIC_KEY=debug; \
	export PIR_API_RECAPTCHA_PRIVATE_KEY=debug; \
	export PIR_API_NOCAPTCHA=false; \
	export PIR_AWS_ACCESS_KEY_ID=secret; \
	export PIR_AWS_SECRET_ACCESS_KEY=test; \
	export PIR_AWS_DEFAULT_REGION=eu-west-1; \
	export PIR_AWS_STORAGE_BUCKET_NAME=pir-invest; \
	export PIR_API_CRYPTOGRAPHY_DONT_BUILD_RUST=1


docker_test_env_files:
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS)

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep invest_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_debug: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	docker-compose pull && \
	docker-compose build && \
	docker-compose run --service-ports webserver make django_webserver

docker_webserver_bash:
	docker exec -it invest_webserver_1 sh

docker_test: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-test.yml build && \
	docker-compose -f docker-compose-test.yml run sut

docker_build:
	docker build -t ukti/invest:latest .

DEBUG_SET_ENV_VARS := \
	export DB_NAME=invest_pir_api_debug; \
	export DB_USER=debug; \
	export DB_PASSWORD=debug; \
	export DATABASE_URL=postgres://debug:debug@localhost:5432/invest_pir_api_debug; \
	export PORT=8014; \
	export DEBUG=true ;\
	export SECRET_KEY=secret; \
	export SESSION_COOKIE_SECURE=false; \
	export SECURE_HSTS_SECONDS=0; \
	export SECURE_SSL_REDIRECT=false; \
	export RECAPTCHA_PUBLIC_KEY=debug; \
	export RECAPTCHA_PRIVATE_KEY=debug; \
	export NOCAPTCHA=false; \
	export CRYPTOGRAPHY_DONT_BUILD_RUST=1; \
	export REDIS_URL=redis://redis:6379; \

DEBUG_CREATE_DB := \
	psql -h localhost -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$$DB_NAME'" | \
	grep -q 1 || psql -h localhost -U postgres -c "CREATE DATABASE $$DB_NAME"; \
	psql -h localhost -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$$DB_USER'" | \
	grep -q 1 || echo "CREATE USER $$DB_USER WITH PASSWORD '$$DB_PASSWORD'; GRANT ALL PRIVILEGES ON DATABASE \"$$DB_NAME\" to $$DB_USER; ALTER USER $$DB_USER CREATEDB" | psql -h localhost -U postgres

debug_db:
	$(DEBUG_SET_ENV_VARS) && $(DEBUG_CREATE_DB)

debug_migrate:
	$(DEBUG_SET_ENV_VARS) && ./manage.py migrate

debug_createsuperuser:
	$(DEBUG_SET_ENV_VARS) && ./manage.py createsuperuser

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) --cov-report=html

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug: test_requirements debug_test

compile_requirements:
	python3 -m piptools compile requirements.in

compile_test_requirements:
	python3 -m piptools compile requirements_test.in

compile_all_requirements: compile_requirements compile_test_requirements

compile_css:
	./node_modules/.bin/gulp css

.PHONY: build clean test_requirements docker_run docker_debug docker_webserver_bash docker_test debug_webserver debug_test debug heroku_deploy_dev
