# -*- encoding: utf-8 -*-

import asyncio
import logging

from django import forms

from core import const
from myhome.api import register_component


REQUIREMENTS = ['python-telegram-bot', 'PySocks']


logger = logging.getLogger(__name__)

# config = dict(
#     token = '618430543:AAHagGT853T1v_x1TlhgYLVy0SxyfpwlgUc',
#     proxy_url = 'socks5://94.130.6.244:1080',
#     proxy_params = {'username': 'friends', 'password': 'asdfghjkl'},
#     chat_id = 41129935,
# )


def register():
    register_component({
        'name': 'Телеграм',
    })


class ComponentSetupForm(forms.Form):
    token = forms.CharField(label='Токен', max_length=100)
    proxy_url = forms.CharField(max_length=100, required=False)
    proxy_user = forms.CharField(max_length=100, required=False)
    proxy_password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)


async def aio_initiate(engine, component):
    await asyncio.sleep(1)
    print('telegram')

    config = component.data

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
    config['command'] = {r['command']: r for r in db}

    bot = TelegramBot(config)

    @engine.eventbus.listen(const.EVENT_START_ENGINE)
    def _start_polling():
        bot.start_polling()

    # engine.eventbus.async_listen_once('start_engine', bot.start_polling)

    return True


class ScriptError(Exception):
    pass


def send_message(mess):
    raise ScriptError(mess)


class TelegramBot:
    def __init__(self, config):
        from telegram import Bot
        from telegram.utils.request import Request
        from telegram.ext import Updater, MessageHandler, Filters

        if config.get('proxy_url'):
            proxy_params = {'username': config.get('proxy_user'), 'password': config.get('proxy_password')}
            request = Request(con_pool_size=8, proxy_url=config['proxy_url'], urllib3_proxy_kwargs=proxy_params)
        else:
            request = Request(con_pool_size=8)

        self.command = config.get('command')
        self.chat_id = config.get('chat_id')
        self.bot = Bot(token=config.get('token'), request=request)
        self.updater = Updater(bot=self.bot, workers=4)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.all, self.polling_callb))

    def send_message(self, text):
        self.bot.send_message(self.chat_id, text)

    def start_polling(self):
        logger.info('TelegramBot start polling...')
        self.updater.start_polling()

    def stop_polling(self):
        self.updater.stop()

    def polling_callb(self, bot, update):
        mes = None
        req = update.message.text
        if req in self.command:
            etype = self.command[req]['type']
            ebody = self.command[req]['body']
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

    # def process_update(self, bot, update):
    #     self.process_message(update.to_dict())
