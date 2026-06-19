#!/bin/sh
set -e

echo "Veritabani migrasyonlari calistiriliyor..."
python /uygulama/Backend/manage.py migrate --noinput

echo "Statik dosyalar toplaniyor..."
python /uygulama/Backend/manage.py collectstatic --noinput

echo "Uygulama ayaga kaldiriliyor..."
gunicorn kalp_yetmezligi.wsgi:application --bind 0.0.0.0:8000 --chdir /uygulama/Backend
