# import os
# import sys
# sys.path.append('{}/../../'.format(os.path.dirname(os.path.abspath(__file__))))

from components.telegram_bot import telebot, chat_id

telebot.send_message(chat_id, 'test')
