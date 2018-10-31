from telegram.ext import Updater, MessageHandler, Filters

from ut import telebot

import os, django, sys
sys.path.append('{}/../../'.format(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")
django.setup()

from myhome.models import Component

comp = Component.objects.get(name='telegram_bot')
print(comp.data)


class ScriptError(Exception):
    pass


def send_message(mess):
    raise ScriptError(mess)


updater = Updater(bot=telebot)


db = [
    {
        'name': 'ip',
        'command': 'ip',
        'type': 'script',
        'body': """import requests;resp = requests.get('https://api.ipify.org/');send_message(resp.text)""",
    },
    {
        'name': 'simple',
        'command': 'hello',
        'type': 'text',
        'body': 'world',
    }
]

conf = {r['command']: r for r in db}


def callb(bot, update):
    mes = None
    req = update.message.text
    if req in conf:
        etype = conf[req]['type']
        ebody = conf[req]['body']
        if etype == 'text':
            mes = ebody
        elif etype == 'script':
            try:
                exec(ebody)
            except ScriptError as e:
                mes = str(e)
            except Exception as e:
                mes = 'ERROR: {}'.format(str(e))

    if mes:
        update.message.reply_text(mes)


updater.dispatcher.add_handler(MessageHandler(Filters.all, callb))
updater.start_polling()
# updater.idle()
