# -*- coding: utf-8 -*-
# Example code for telegrambot.py module
from telegram.ext import CommandHandler, MessageHandler, Filters, RegexHandler, typehandler
from telegram import ParseMode
from django_telegrambot.apps import DjangoTelegramBot
from Log.Log import Log
import datetime
from django.utils import timezone
from telegram.chataction import ChatAction
from TelegramAdmin.Authentication import UserController
from TelegramAdmin.models import UserSearch
from FileManager.FileManager import FileController
from FileManager.models import File


logger = Log('KelasorBot', level=10)
logger.info("Bot Started")

user_controller = UserController()
file_controller = FileController()
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
STATS = None
NEXT_STATS = None
logger.telegram("bot started")

def get_message(message):
    with open("Messages/"+message, 'r', encoding='utf-8-sig') as f:
        return "".join(f.readlines())

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'Kb', 2: 'Mb', 3: 'Gb'}
    while size > power:
        size /= power
        n += 1
    return '%.2f' % (size) + power_labels[n]


def start_back(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text=get_message('start_msg'))


def start_handler(bot, update):
    try:
        user_controller.update_create_user(update.message.chat)
        logger.debug("User \n{}\n\n start the bot".format(update.message.chat))
        start_back(bot, update)
    except Exception as e:
        logger.error("start : {}".format(e))


def help_hadler(bot, update):
    user_controller.update_create_user(update.message.chat)
    bot.sendMessage(update.message.chat_id, text='Help!')


def upload_file_handler(bot, update):
    try:
        user = user_controller.update_create_user(update.message.chat)
        file_id = file_controller.save(update.message, user)
        logger.debug("User {} upload file {}".format(user.chat_id, file_id))
        msg = get_message('after_upload_file') + '\n' + '/kelasor_{}'.format(file_id)
        bot.sendMessage(update.message.chat_id, text=msg)
    except Exception as e:
        logger.error("upload_file : {}".format(e))


def get_file_handler(bot, update):
    try:
        logger.debug("Getting file {}".format(update.message.text))
        file = file_controller.get(update.message.text.replace('/kelasor_', ''))
        desc = file.file_description + '\n@kelasorbot'
        bot.send_document(update.message.chat_id, file.file_id, caption=desc)
    except Exception as e:
        logger.error("get_file : {}".format(e))


def text_handler(bot, update):
    try:
        user = user_controller.update_create_user(update.message.chat)
        STATES[user.state](bot, update, user)
    except Exception as e:
        logger.error("text_handler : {}".format(e))


def search_file(bot, update, user):
    try:
        query = update.message.text
        logger.debug("User {} search file {}".format(user.chat_id, query))
        files = File.objects.filter(file_name__search=query).all()
        response = 'success'
        search_res = []
        if not files:
            response = 'failed'
            bot.sendMessage(update.message.chat_id, 'همچین فایلی پیدا نشد. لطفا با جست‌وجو دقیق‌تر دوباره امتحان کنید.')
        else:
            for file in files:
                size = format_bytes(file.file_size)
                if len(file.file_name) > 10:
                    msg = '{}\n💾{} - 📥/bp_{}'.format(file.file_name,
                                                       size,
                                                            file.id)
                else:
                    desc = file.file_description.replace('\n', ' ')[:20] + '...'
                    msg = '{} - {}\n💾{} - 📥/bp_{}'.format(file.file_name,
                                                           desc,
                                                            size,
                                                           file.id)
                search_res.append(msg)
            bot.sendMessage(update.message.chat_id, '\n\n'.join(search_res[:10]))
        UserSearch(user=user,
                   query=query,
                   response=response,
                   search_result=search_res).save()
    except Exception as e:
        logger.error("search_file : {}".format(e))


STATES = {
    'start': start_handler,
    'search_file': search_file
}
NEXT_STATES = {
    'start': 'search_file',
    'search_file': 'search_file'

}
user_controller.set_next_states_dict(NEXT_STATES)


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.TELEGRAM_BOT_TOKENS)
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("help", help_hadler))
    dp.add_handler(MessageHandler(Filters.document, upload_file_handler))
    dp.add_handler(RegexHandler('^/kelasor', get_file_handler))
    dp.add_handler(MessageHandler(Filters.text, text_handler))



