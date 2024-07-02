from telebot import types

def useful_links():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [
        types.KeyboardButton('Полезные таблицы'),
        types.KeyboardButton('Полезные статьи'),
        types.KeyboardButton('Работа с сервисом Grafana'),
        types.KeyboardButton('Ссылки на чаты')
    ]
    markup.add(*buttons)
    return markup

def create_links_keyboard(links):
    keyboard = types.InlineKeyboardMarkup()
    for link in links:
        button = types.InlineKeyboardButton(text=link['title'], url=link['url'])
        keyboard.add(button)
    return keyboard

def communication_inlaine_keyboards():
    type_communications = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Наблюдается ошибка', callback_data='error_communication'),
        types.InlineKeyboardButton('Для информации', callback_data='attention_communication'),
        types.InlineKeyboardButton('Ошибка исправлена', callback_data='fixed_communication')
    ]
    type_communications.add(*buttons)
    return type_communications

def create_priority_keyboard(priorities):
    keyboard = types.InlineKeyboardMarkup()
    for priority in priorities:
        button = types.InlineKeyboardButton(text=priority, callback_data=priority)
        keyboard.add(button)
    return keyboard