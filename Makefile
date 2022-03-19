SHELL := /bin/bash

build:
	docker-compose build

stop:
	docker-compose stop

run:
	docker-compose up

down:
	docker-compose down -v

black:
	docker-compose exec app black .

flake8:
	docker-compose exec app flake8 .

makemigrations:
	docker-compose exec app python manage.py makemigrations

migrate:
	docker-compose exec app python manage.py migrate

admin:
	docker-compose exec app python manage.py createsuperuser
