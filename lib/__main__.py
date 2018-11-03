import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

from components.telegram_bot import polling, registration

# polling.set_plato()

registration.setup_component()
