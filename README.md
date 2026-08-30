# Helpdesk-API
This project is design for user who faced issued from service and want to help from company.
# Install the Django
```bash
pip install Django
```
# For Django initial step
```bash
django-admin startproject config .
```
# Check it wrok successfully or not
```bash
python manage.py check
```
# Run the project
```bash
python manage.py runserver
```
# create folder
```bash
mkdir -p config/settings
```
# Check the settings
```bash
python manage.py check --settings=config.settings.development
python manage.py check --settings=config.settings.testing
python manage.py check --settings=config.settings.production
```
# Setup MySql database
```bash
DB_NAME=helpdesk # create database via mysql workbranch
DB_USER=root # write the username
DB_PASSWORD=mysql # write the password
DB_HOST=127.0.0.1 # write allowed host address
DB_PORT=3306 # write allowed port number
```

# Create Django app
```bash
# first create apps/users folders
python manage.py startapp users apps/users
```

# Verify database connectivity through Django shell
```bash
Run:

python manage.py shell

Then:

from django.db import connection

connection.vendor

Expected:

'mysql'

Then:

connection.settings_dict["NAME"]

Expected:

'helpdesk'

Then:

from apps.users.models import User

User.objects.count()

If you created your superuser and test users in Step 3, this should return the corresponding count.

Exit:

exit()
```
# Generate random JWT secret
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```


# HelpDesk API

Production-oriented REST API for a support/helpdesk platform.

## Overview

The HelpDesk API provides:

- customer registration and authentication;
- role-based authorization;
- ticket management;
- category management;
- ticket assignment;
- ticket workflow;
- comments;
- SLA/overdue handling;
- dashboard statistics;
- audit logging;
- OpenAPI/Swagger documentation.

## Technology Stack

- Python
- Django
- Django REST Framework
- MySQL
- Redis
- Celery
- Docker
- Nginx
- Gunicorn
- JWT
- OpenAPI / Swagger
- pytest

## Architecture

```text
Client
  |
  v
Nginx
  |
  v
Gunicorn
  |
  v
Django REST Framework
  |
  +-------------------+
  |                   |
  v                   v
MySQL                Redis
                      |
                  +---+---+
                  |       |
               Celery   Beat
