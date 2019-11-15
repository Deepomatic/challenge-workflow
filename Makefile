all: migrate
	python3 challenge/manage.py runserver 0.0.0.0:8000

migrate:
	python3 challenge/manage.py migrate

start:
	python3 challenge/manage.py runserver 0.0.0.0:8000

test:
	python3 challenge/manage.py test challenge/api/