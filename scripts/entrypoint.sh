#!/bin/sh

set -e

cd inventoryproject

python manage.py collectstatic --noinput

uwsgi --socket :8000 --master --enable-threads --module inventoryproject.wsgi
