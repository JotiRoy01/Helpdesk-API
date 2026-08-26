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
