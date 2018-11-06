#!/usr/bin/env python

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

import importlib
import re
import subprocess

paths = subprocess.Popen("grep -r -l register_component lib/components/ | grep -p '.py$'", shell=True, stdout=subprocess.PIPE)
for p in paths.stdout.readlines():
    file = re.sub(r'(^lib/)|((/__init__)?\.py\n$)', '', p.decode('utf-8'))
    file = re.sub(r'(/{1,})', '.', file)

    try:
        module = importlib.import_module('{}'.format(file))
    except ModuleNotFoundError:
        raise()

    module.register()
