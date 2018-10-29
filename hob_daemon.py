# -*- encoding: utf-8 -*-

import daemon


logfile = open('daemon.log', 'w')

with daemon.DaemonContext(stdout=logfile, stderr=logfile):
    import requests
    import telebot

    bot = telebot.TeleBot('618430543:AAHagGT853T1v_x1TlhgYLVy0SxyfpwlgUc')
    chat_id = 41129935

    @bot.message_handler(commands=['ip'])
    def send_welcome(message):
        resp = requests.get('https://api.ipify.org/')
        bot.send_message(chat_id, resp.text)

    bot.polling(none_stop=False, interval=0, timeout=30)
