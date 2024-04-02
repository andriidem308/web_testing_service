MANAGE = python3 src/manage.py
PROJECT_DIR = $(shell pwd)
WSGI_PORT=8081

# <---------- RUN ---------->
run:
	$(MANAGE) runserver 0.0.0.0:8000

gunicorn_run:
	gunicorn -w 1 -b 0.0.0.0:$(WSGI_PORT) --chdir $(PROJECT_DIR)/src core.wsgi --timeout 30 --log-level debug --max-requests 10000

gunicorn_run_8082:
	gunicorn -w 1 -b 0.0.0.0:8082 --chdir $(PROJECT_DIR)/src core.wsgi --timeout 30 --log-level debug --max-requests 10000

gunicorn-sock:
	gunicorn -w 1 -b unix:/tmp/gunicorn.sock --chdir $(PROJECT_DIR)/src core.wsgi --timeout 30 --log-level debug --max-requests 10000

# <------------------------->

# ---------> Migrations <---------
migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

migrate_acc:
	$(MANAGE) makemigrations accounts

migrate_main:
	$(MANAGE) makemigrations main
# <------------------------->

# ---------> Nginx <---------
run_nginx:
	systemctl start nginx

stop_nginx:
	systemctl stop nginx

reload_nginx:
	systemctl reload nginx
# <------------------------->


# <------------------------->
collect-static:
	$(MANAGE) collectstatic

requirements:
	pip install -r requirements.txt

superuser:
	$(MANAGE) createsuperuser

app:
	$(MANAGE) startapp $(app)

lint:
	flake8 .
# <------------------------->