import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

import importlib

from myhome import models


qs = models.Component.objects.filter(is_active=True)
for c in qs:
    try:
        module = importlib.import_module('components.{}'.format(c.name))
    except ModuleNotFoundError:
        raise()

    module.run()
