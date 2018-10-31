from telegram.ext import Updater, MessageHandler, Filters

from components.telegram_bot import bot_init


def set_plato():
    bot = bot_init()
    pol = TelePoll(bot)
    pol.start_polling()


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


class ScriptError(Exception):
    pass


def send_message(mess):
    raise ScriptError(mess)


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


class TelePoll():
    def __init__(self, bot):
        self.updater = Updater(bot=bot, workers=4)

        self.updater.dispatcher.add_handler(MessageHandler(Filters.all, callb))
        # self.updater.dispatcher.add_error_handler(process_error)

    def start_polling(self):
        self.updater.start_polling()

    def stop_polling(self):
        self.updater.stop()

    def process_update(self, bot, update):
        self.process_message(update.to_dict())
