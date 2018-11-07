# -*- encoding: utf-8 -*-

import asyncio

from django import forms

from myhome.api import register_component, get_component_config

from telegram import Bot
from telegram.utils.request import Request


def register():
    register_component({
        'human_name': 'Телеграм',
    })


class ComponentSetupForm(forms.Form):
    token = forms.CharField(label='Токен', max_length=100)
    proxy_url = forms.CharField(max_length=100, required=False)
    proxy_user = forms.CharField(max_length=100, required=False)
    proxy_password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)


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
    config = get_component_config()

    token = config['token']
    proxy_url = config['proxy_url']
    proxy_params = config['proxy_params']
    # chat_id = config['chat_id']

    if proxy_url is not None:
        request = Request(con_pool_size=8, proxy_url=proxy_url, urllib3_proxy_kwargs=proxy_params)
    else:
        request = Request(con_pool_size=8)

    return Bot(token=token, request=request)


def run():
    print('yyyeeee')


async def aio_run():
    await asyncio.sleep(1)
    print("telegram_bot")
