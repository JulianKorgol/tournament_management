#!/bin/bash

rm -fv /app/db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py load_db
python manage.py runserver 0.0.0.0:8000
