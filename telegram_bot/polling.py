# -*- encoding: utf-8 -*-

import requests

from telegram.ext import Updater, MessageHandler, Filters

from ut import telebot

updater = Updater(bot=telebot)


def ip(bot, update):
    resp = requests.get('https://api.ipify.org/')
    update.message.reply_text(resp.text)


def callb(bot, update):
    req = update.message.text
    if req in ['/ip', 'ip']:
        resp = requests.get('https://api.ipify.org/')
        update.message.reply_text(resp.text)


updater.dispatcher.add_handler(MessageHandler(Filters.all, callb))
updater.start_polling()
# updater.idle()
