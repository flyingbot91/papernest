# Networking coverage

## Installation
	- Download the repo (git clone ...)
	- cd <repo>
	- /usr/bin/python -m venv env
	- source env/bin/activate
	- python -m pip install --upgrade pip
	- python -m pip install -r requirements.txt
	- python manage.py makemigrations
	- python manage.py migrate

## Ingest data
	- python manage.py ingest_data <CSV_FILE>

## Run server
	- python manage.py runserver
