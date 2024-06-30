from telebot import types
from Database.database import DatabaseManager


session = DatabaseManager.get_session()

class ButtonConstructor:
    def __init__(self, button_data=None, links=None):
        """
        Конструктор кнопок и ссылок.
        :param button_data: список словарей с данными кнопок. Каждый словарь должен содержать ключи 'text' и 'callback_data'.
        :param links: список словарей с данными ссылок. Каждый словарь должен содержать ключи 'title' и 'url'.
        """
        self.button_data = button_data if button_data is not None else []
        self.links = links if links is not None else []

    def get_markup(self):
        """
        Возвращает объект InlineKeyboardMarkup с созданными кнопками и ссылками.
        """
        markup = types.InlineKeyboardMarkup()
        # Добавление кнопок
        for btn in self.button_data:
            button = types.InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data'])
            markup.add(button)
        # Добавление ссылок
        for link in self.links:
            button = types.InlineKeyboardButton(text=link['title'], url=link['url'])
            markup.add(button)
        return markup

# Пример использования
button_data = [
    {'text': 'Кнопка 1', 'callback_data': 'button1'},
    {'text': 'Кнопка 2', 'callback_data': 'button2'},
]

links = [
    {'title': 'Google', 'url': 'https://google.com'},
    {'title': 'GitHub', 'url': 'https://github.com'},
]

buttons_and_links = ButtonConstructor(button_data=button_data, links=links)
markup = buttons_and_links.get_markup()
