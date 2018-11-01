# -*- encoding: utf-8 -*-

from telegram import Bot
from telegram.utils.request import Request

# class TeleBot:
#     def __init__(self):

#         comp = Component.objects.get(name='telegram_bot')
#         config = comp.data

#         token = config['token']
#         proxy_url = config['proxy_url']
#         proxy_params = config['proxy_params']
#         chat_id = config['chat_id']

#         if proxy_url is not None:
#             request = Request(con_pool_size=8, proxy_url=proxy_url, urllib3_proxy_kwargs=proxy_params)
#         else:
#             request = Request(con_pool_size=8)

#         self.bot = Bot(token=token, request=request)
#         self.chat_id = chat_id

#     def send_message(self, text):
#         self.bot.send_message(self.chat_id, text)


def bot_init():
    from myhome.models import Component

    comp = Component.objects.get(name='telegram_bot')
    config = comp.data

    token = config['token']
    proxy_url = config['proxy_url']
    proxy_params = config['proxy_params']
    # chat_id = config['chat_id']

    if proxy_url is not None:
        request = Request(con_pool_size=8, proxy_url=proxy_url, urllib3_proxy_kwargs=proxy_params)
    else:
        request = Request(con_pool_size=8)

    return Bot(token=token, request=request)
