MANAGE = python3 manage.py

run:
	$(MANAGE) runserver

makemigrations:
	$(MANAGE) makemigrations

migrate_acc:
	$(MANAGE) makemigrations accounts

migrate_main:
	$(MANAGE) makemigrations main

migrate:
	$(MANAGE) migrate

requirements:
	pip install -r requirements.txt

admin:
	$(MANAGE) createsuperuser

app:
	$(MANAGE) startapp $(app)