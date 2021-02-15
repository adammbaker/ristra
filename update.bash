#!/usr/bin/env bash
source venv/bin/activate
pip install -r -U requirements.txt
python manage.py migrate
source venv/bin/activate
python manage.py collectstatic --noinput
