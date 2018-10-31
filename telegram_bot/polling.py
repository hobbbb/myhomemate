# -*- encoding: utf-8 -*-

# import requests

from telegram.ext import Updater, MessageHandler, Filters

from ut import telebot

updater = Updater(bot=telebot)


# if req in ['/ip', 'ip']:
#     resp = requests.get('https://api.ipify.org/')
#     update.message.reply_text(resp.text)
db = [
    {
        'name': 'ip',
        'command': 'ip',
        'type': 'script',
        'body': """import requests;resp = requests.get('https://api.ipify.org/');resp.text""",
    },
    {
        'name': 'simple',
        'command': 'hello',
        'type': 'text',
        'body': 'world',
    }
]

conf = {r['command']: r for r in db}

scr = """import requests;resp = requests.get('https://api.ipify.org/');mes = resp.text"""
res = exec(scr)
print(res)

exit()


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
                mes = exec(ebody)
            except Exception as e:
                mes = str(e)

    if mes:
        update.message.reply_text(mes)


updater.dispatcher.add_handler(MessageHandler(Filters.all, callb))
updater.start_polling()
# updater.idle()
