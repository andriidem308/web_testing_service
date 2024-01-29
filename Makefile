MANAGE = python3 manage.py

run:
	$(MANAGE) runserver

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

requirements:
	pip install -r requirements.txt

admin:
	$(MANAGE) createsuperuser