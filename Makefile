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

delete_branches:
	(git branch | grep -v "main" | xargs git branch -D)

pull_and_delete:
	git checkout main && git pull && make delete_branches