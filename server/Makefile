build:
	docker-compose build

up:
	docker-compose up -d

up-non-daemon:
	docker-compose up

migrate:
	docker-compose run web python3 manage.py migrate

loaddata:
	docker-compose run web python3 manage.py loaddata load_data.json

superuser:
	docker-compose run web python3 manage.py createsuperuser

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

test:
	docker-compose run web python3 manage.py test
