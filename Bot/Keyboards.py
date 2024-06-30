from telebot import types


def useful_links():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton('Полезные таблицы')
    button2 = types.KeyboardButton('Полезные статьи')
    button3 = types.KeyboardButton('Работа с сервисом Grafana')
    button4 = types.KeyboardButton('Ссылки на чаты')
    markup.add(button1, button2, button3, button4)
    return markup

def create_links_keyboard(links):
    keyboard = types.InlineKeyboardMarkup()
    for link in links:
        button = types.InlineKeyboardButton(text=link['title'], url=link['url'])
        keyboard.add(button)
    return keyboard

def communication_inlaine_keyboards():
    type_communications = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Наблюдается ошибка', callback_data='error_communication')
    button2 = types.InlineKeyboardButton('Для информации', callback_data='attention_communication')
    button3 = types.InlineKeyboardButton('Ошибка исправлена', callback_data='fixed_communication')
    type_communications.add(button1, button2, button3)
    return type_communications

def create_priority_keyboard(priorities):
    keyboard = types.InlineKeyboardMarkup()
    for priority in priorities:
        button = types.InlineKeyboardButton(text=priority, callback_data=priority)
        keyboard.add(button)
    return keyboard

