import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kalp_yetmezligi.settings")

uygulama = get_wsgi_application()
application = uygulama
