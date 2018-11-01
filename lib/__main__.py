import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

from components.telegram_bot import polling

polling.set_plato()
