import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

from components import telegram_bot
from components.devices import mikrotik
from components.devices.mikrotik import scanner

telegram_bot.register()
mikrotik.register()

# telegram_bot.polling.set_plato()

scanner.test()
