import json
import random
from telebot import types
from Bot.Keyboards import create_links_keyboard, useful_links, communication_inlaine_keyboards, create_priority_keyboard
from Database.database import DatabaseManager

class MainBot:
    def __init__(self):
        self.dbmanager = DatabaseManager()
        self.user_states = {}
        self.links_data = self.load_links_data('Servicies/Data.json')
        self.test_data = self.load_links_data('Servicies/Test_cases.json')

    def load_links_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle_start(self, bot, message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name if message.from_user.first_name else "NoFirstName"
        self.dbmanager.add_user(user_id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        welcome_text = f'Привет, {first_name}! Я бот-помощник технического администратора.'
        bot.send_message(message.chat.id, welcome_text)

    def handle_useful_links(self, bot, message):
        help_buttons = useful_links()
        bot.send_message(message.chat.id, "Выберите команду:", reply_markup=help_buttons)

    def handle_test_cases(self, bot, message):
        user_id = message.chat.id
        self.user_states[user_id] = {'current_case': 0, 'correct_answers': 0}
        self.send_next_case(bot, message)

    def send_next_case(self, bot, message):
        user_id = message.chat.id
        current_case_index = self.user_states[user_id]['current_case']
    
        if current_case_index < len(self.test_data['cases']):
            random_case = self.test_data['cases'][current_case_index]
            case_number = random_case['number']
            case_text = random_case['text']
            correct_priority = random_case['priority_name']
        
            priorities = self.dbmanager.get_priorities()
        
            if isinstance(priorities, list):
                options = random.sample(priorities, min(4, len(priorities)))
                if correct_priority not in options:
                    options.pop()
                    options.append(correct_priority)
            
                markup = create_priority_keyboard(options)
                self.user_states[user_id]['correct_priority'] = correct_priority
            
                bot.send_message(user_id, f"Тестовый кейс #{case_number}: {case_text}\nВыберите правильный приоритет:", reply_markup=markup)
            else:
                bot.send_message(user_id, "Ошибка: Неверный формат приоритетов.")
        else:
            correct_answers = self.user_states[user_id].get('correct_answers', 0)
            bot.send_message(user_id, f"Все тестовые кейсы пройдены. Правильных ответов: {correct_answers} из {len(self.test_data['cases'])}. Спасибо за участие!")
            del self.user_states[user_id]

    def handle_answer(self, bot, call):
        user_id = call.message.chat.id
        if user_id in self.user_states:
            selected_priority = call.data
            correct_priority = self.user_states[user_id].get('correct_priority', None)
            current_case_index = self.user_states[user_id].get('current_case', 0)
            test_case_id = self.test_data['cases'][current_case_index]['number'] 

            is_correct = selected_priority == correct_priority

            self.dbmanager.record_test_case_result(user_id, test_case_id, is_correct)

            if is_correct:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Верно! Вы выбрали правильный приоритет.")
                self.user_states[user_id]['correct_answers'] = self.user_states[user_id].get('correct_answers', 0) + 1
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Неверно! Попробуйте еще раз.")

            self.user_states[user_id]['current_case'] = self.user_states[user_id].get('current_case', 0) + 1
            self.send_next_case(bot, call.message)
        else:
            bot.send_message(user_id, "Ошибка: Пользователь не найден в состоянии.")

    def handle_create_communication(self, bot, message):
        communication_buttons = communication_inlaine_keyboards()
        bot.send_message(message.chat.id, "Выберите тип коммуникации:", reply_markup=communication_buttons)

    def handle_text(self, bot, message):
        if message.text == 'Полезные таблицы':
            keyboard = create_links_keyboard(self.links_data['tables'])
            bot.send_message(message.chat.id, "Выберите таблицу:", reply_markup=keyboard)
        elif message.text == 'Полезные статьи':
            keyboard = create_links_keyboard(self.links_data['books'])
            bot.send_message(message.chat.id, "Выберите статью:", reply_markup=keyboard)
        elif message.text == 'Работа с сервисом Grafana':
            keyboard = create_links_keyboard(self.links_data['grafana'])
            bot.send_message(message.chat.id, "Ссылка на дашборд и инструкция к нему:", reply_markup=keyboard)
        elif message.text == 'Ссылки на чаты':
            keyboard = create_links_keyboard(self.links_data['chatbots'])
            bot.send_message(message.chat.id, "Ссылки на чаты:", reply_markup=keyboard)

    def handle_callback(self, bot, call):
        if call.data == 'error_communication':
            bot.send_message(call.message.chat.id, "Введите сообщение об ошибке:")
            bot.register_next_step_handler(call.message, lambda message: self.process_error_communication_step(bot, message))
        elif call.data == 'attention_communication':
            bot.send_message(call.message.chat.id, "Введите сообщение для внимания:")
            bot.register_next_step_handler(call.message, lambda message: self.process_attention_communication_step(bot, message))
        elif call.data == 'fixed_communication':
            bot.send_message(call.message.chat.id, "Введите сообщение об исправленной ошибке:")
            bot.register_next_step_handler(call.message, lambda message: self.process_fixed_communication_step(bot, message))

    def process_error_communication_step(self, bot, message):
        user_text = message.text
        formatted_text = f"‼️ Наблюдается проблема:\n{user_text}"
        bot.send_message(message.chat.id, "Текст готов к копированию:")
        bot.send_message(message.chat.id, formatted_text)

    def process_attention_communication_step(self, bot, message):
        user_text = message.text
        formatted_text = f"⚠️Для информации:\n{user_text}\nВ случае возникновения вопросов обращаться к дежурному второй линии поддержки"
        bot.send_message(message.chat.id, "Текст готов к копированию:")
        bot.send_message(message.chat.id, formatted_text)

    def process_fixed_communication_step(self, bot, message):
        user_text = message.text
        formatted_text = f"✅Исправлено:\n{user_text}"
        bot.send_message(message.chat.id, "Текст готов к копированию:")
        bot.send_message(message.chat.id, formatted_text)