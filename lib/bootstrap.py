#!/usr/bin/env python

import argparse
import importlib
import re
import subprocess

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhome.settings')
django.setup()

from myhome.api import register_component


def get_module_from_path(path):
    file = re.sub(r'(^lib/)|((/__init__)?\.py\n$)', '', path)
    file = re.sub(r'(/{1,})', '.', file)

    try:
        module = importlib.import_module('{}'.format(file))
    except ModuleNotFoundError:
        raise()
    return module


def register():
    paths = subprocess.Popen(
        'grep -r -l NAME lib/components/ | grep -p ".py$"', shell=True, stdout=subprocess.PIPE
    )
    for p in paths.stdout.readlines():
        module = get_module_from_path(p.decode('utf-8'))
        register_component(module)


def setup():
    requirements = set()

    paths = subprocess.Popen(
        'grep -r -l REQUIREMENTS lib/components/ | grep -p ".py$"', shell=True, stdout=subprocess.PIPE
    )
    for p in paths.stdout.readlines():
        module = get_module_from_path(p.decode('utf-8'))
        for r in module.REQUIREMENTS:
            requirements.add(r)

    for r in [
        'asyncio',
        'uvloop',
        'requests',
        'django-bootstrap4',
        'jsonfield',
        'Django==2.1.2',
        'mysqlclient==1.3.13',
        'python3-memcached',
        'APScheduler',
    ]:
        requirements.add(r)

    subprocess.call(['pip', 'install'] + list(requirements))


def drop():
    """ FOR DEVELOPING """
    mysql = ['mysql', '-uroot', 'myhome', '-e']
    subprocess.call(mysql + ['delete from django_migrations where app="myhome"'])
    for t in ['zone', 'service', 'entity', 'device', 'component']:
        subprocess.call(mysql + [f'drop table myhome_{t}'])


parser = argparse.ArgumentParser()
parser.add_argument('--register', action='store_true')
parser.add_argument('--setup', action='store_true')
parser.add_argument('--drop', action='store_true')
args = parser.parse_args()

if args.register is True:
    register()
elif args.setup is True:
    setup()
elif args.drop is True:
    drop()
