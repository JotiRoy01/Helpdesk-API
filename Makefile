install:
	pip install -r requirements.txt

check:
	python manage.py check

migrations:
	python manage.py makemigrations --check

test:
	pytest -v

test-unit:
	pytest -m unit -v

test-integration:
	pytest -m integration -v

test-security:
	pytest -m security -v

test-performance:
	pytest -m performance -v

coverage:
	pytest --cov=apps --cov-report=term-missing

run:
	python manage.py runserver

schema:
	python manage.py spectacular --file schema.yml

schema-check:
	python manage.py spectacular --validate