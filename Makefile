
activate:
	poetry shell

install/python:
	poetry install

copy/local/envs:
	cd server && cp .env.dev .env

run/migrate:
	python server/manage.py migrate

run/django:
	python server/manage.py runserver 0.0.0.0:8000

run/tests:
	poetry run pytest -x server/

ci: copy/local/envs run/tests
