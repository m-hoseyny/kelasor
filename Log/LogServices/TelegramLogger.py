import logging, os
from telegram.ext import Updater


class TelegramSendLogHandler(logging.Handler):
    def __init__(self, token, bot=None, chat_id_list=[], *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        if bot is None:
            self.updater = Updater(token)
            bot = self.updater.bot
        self.bot = bot
        self.chat_id_list = chat_id_list
        if type(chat_id_list) is not list:
            self.chat_id_list = [chat_id_list]
        
    def emit(self, record):
        try:
            for chat_id in self.chat_id_list:
                try:
                    msg = self.format(record)
                    self.bot.send_message(chat_id = chat_id, text = msg)
                except Exception as e:
                    print(e)
                    print("Bot Not Defined")

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def send_message(self, msg):
        for chat_id in self.chat_id_list:
            try:
                self.bot.send_message(chat_id=chat_id, text=msg)
            except Exception as e:
                print(e)
                print("Bot Not Defined")
