import logging, os
import requests
from threading import Thread


class Jacondatori(logging.Handler):
    def __init__(self, bot = None, chat_id_list = [], *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.requests = requests.session()
        self.API = 'https://cafechap.com/bot/api/v1/endpoint/groups/-367993500/messages?token=cQq1b3qEGkYhNw2OC3SWKcAo6GqFep&text='
        
    def emit(self, record):
        try:
            msg = self.format(record)
            th = Thread(target=self.send_message, args=(msg,))
            th.start()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def send_message(self, msg):
        try:
            msg = msg.replace('#', '')
            self.requests.get(self.API + str(msg))
        except Exception as e:
            print(str(e))
