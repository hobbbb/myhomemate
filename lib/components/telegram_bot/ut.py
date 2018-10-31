# -*- encoding: utf-8 -*-

from telegram import Bot
from telegram.utils.request import Request


token = '618430543:AAHagGT853T1v_x1TlhgYLVy0SxyfpwlgUc'
proxy_url = 'socks5://94.130.6.244:1080'
proxy_params = {'username': 'friends', 'password': 'asdfghjkl'}
chat_id = 41129935


if proxy_url is not None:
    request = Request(con_pool_size=8, proxy_url=proxy_url, urllib3_proxy_kwargs=proxy_params)
else:
    request = Request(con_pool_size=8)


telebot = Bot(token=token, request=request)

# class TeleBot:
#     def __init__(self):
#         self.bot = Bot(token=token, request=request)
#         self.chat_id = chat_id
