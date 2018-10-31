
from telegram.ext import Updater, MessageHandler, Filters

from ut import telebot


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
            except Exception as e:
                mes = str(e)

    if mes:
        update.message.reply_text(mes)


updater.dispatcher.add_handler(MessageHandler(Filters.all, callb))
updater.start_polling()
# updater.idle()
