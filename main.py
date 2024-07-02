import telebot
from telebot import types
from Bot.main_bot import MainBot
from Bot.admin_bot import AdminBot
from Database.database import DatabaseManager
from Config.config import read_json


config_path = 'Config/config.json'
config = read_json(config_path)
bot_token = config['telegram']['key']

bot = telebot.TeleBot(bot_token)

dbmanager = DatabaseManager()
mainbot = MainBot()
adminbot = AdminBot(bot)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    mainbot.handle_start(bot, message)

# Обработчик команды /useful_links
@bot.message_handler(commands=['useful_links'])
def help_message(message):
    mainbot.handle_useful_links(bot, message)

# Обработчик команды /create_communication
@bot.message_handler(commands=['create_communication'])
def communication_command(message):
    mainbot.handle_create_communication(bot, message)

@bot.message_handler(commands=['test_cases'])
def test_cases_command(message):
    mainbot.handle_test_cases(bot, message)

@bot.message_handler(commands=['admin_panel'])
def admin_panel_command(message):
    adminbot.admin_panel_callback(message)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def text_message(message):
    mainbot.handle_text(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    mainbot.handle_callback(bot, call)
    mainbot.handle_answer(bot, call)


if __name__ == '__main__':
    dbmanager.create_tables()
    dbmanager.load_data_from_json('Servicies/Test_cases.json')
    #dbmanager.add_ptiority()
    
    bot.polling(none_stop=True)