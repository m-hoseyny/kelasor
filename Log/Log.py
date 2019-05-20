import logging, os
from Log.LogServices.TelegramLogger import TelegramSendLogHandler

DEBUG = int(os.getenv('DEBUG', 0))
CHAT_ID = int(os.getenv('REPORT_CHAT_ID'))
TELEGRAM = int(os.getenv("TELEGRAM", 1))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LOG_LEVEL = int(os.getenv("LOG_LEVEL", 20))
TELEGRAM_LOG_LEVEL = int(os.getenv("TELEGRAM_LOG_LEVEL", 30))


class Log:
    def __init__(self, name,  telegram=TELEGRAM, level=LOG_LEVEL, telegram_level=TELEGRAM_LOG_LEVEL):
        self.__name__ = name
        self.logger = logging.getLogger(self.__name__)
        self.logger.setLevel(level)
        self.telegram_flag = telegram
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        logging.addLevelName(25, 'TELEGRAM')
        if self.telegram_flag:
            tslh = TelegramSendLogHandler(token=TELEGRAM_TOKEN, chat_id_list=[CHAT_ID])
            formatter = logging.Formatter('%(asctime)s - #%(name)s - #%(levelname)s - %(message)s')
            tslh.setLevel(telegram_level)
            tslh.setFormatter(formatter)
            self.logger.addHandler(tslh)
            self.msg_log = tslh

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def telegram(self, msg):
        self.info(msg)
        if self.telegram_flag:
            self.msg_log.send_message(msg)

    def send_message_log(self, msg):
        self.msg_log.send_message(msg)
