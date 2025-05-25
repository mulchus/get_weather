#!/bin/bash
set -e

docker-compose build
docker-compose run --rm django ./manage.py migrate
docker-compose run --rm django ./manage.py fill_db
#docker-compose run --rm django ./manage.py createsuperuser  # if you want to create superuser
docker-compose up
