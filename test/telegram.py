# import requests
# import telebot


# bot = telebot.TeleBot('618430543:AAHagGT853T1v_x1TlhgYLVy0SxyfpwlgUc')
# chat_id = 41129935


# @bot.message_handler(commands=['ip'])
# def send_welcome(message):
#     resp = requests.get('https://api.ipify.org/')
#     bot.send_message(chat_id, resp.text)

# def main():
#     bot.polling(none_stop=False, interval=0, timeout=30)




import telegram
print(dir(telegram))
# from telegram.bot import Bot

# bot = Bot(token='618430543:AAHagGT853T1v_x1TlhgYLVy0SxyfpwlgUc')
# print(bot.get_me())
