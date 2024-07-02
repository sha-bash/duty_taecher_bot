import json
from telebot import types
from Database.database import DatabaseManager

class AdminBot:
    def __init__(self, bot):
        self.bot = bot
        self.dbmanager = DatabaseManager()
        self.links_data = self.load_links_data('Servicies/Data.json')
        self.test_data = self.load_links_data('Servicies/Test_cases.json')

    def load_links_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def add_test_case(self, priority_id, text):
        try:
            with open('Servicies/Test_cases.json', 'r') as file:
                data = json.load(file)
                last_number = data[-1]['number'] if data else 0
                new_test_case = {
                    "number": last_number + 1,
                    "priority_id": priority_id,
                    "priority_name": self.dbmanager.get_priorities(),
                    "text": text
                }
                data.append(new_test_case)
            
            with open('Servicies/Test_cases.json', 'w') as file:
                json.dump(data, file, indent=4)
            
            # Загрузка данных в базу данных
            self.dbmanager.load_data_from_json('Servicies/Test_cases.json')
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Ошибка при добавлении тестового кейса: {e}")

    def add_data(self, title, url, data_type):
        try:
            with open('Servicies/Data.json', 'r') as file:
                data = json.load(file)
                new_link = {
                    "title": title,
                    "url": url
                }
                data[data_type].append(new_link)
            
            with open('Servicies/Data.json', 'w') as file:
                json.dump(data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Ошибка при добавлении данных: {e}")

    def delete_test_case(self, test_case_number):
        try:
            with open('Servicies/Test_cases.json', 'r') as file:
                data = json.load(file)
                data = [test_case for test_case in data if test_case['number'] != test_case_number]
            
            with open('Servicies/Test_cases.json', 'w') as file:
                json.dump(data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Ошибка при удалении тестового кейса: {e}")

    def upload_file(self, file_path, directory):
        import shutil
        try:
            shutil.copy(file_path, directory)
        except FileNotFoundError as e:
            print(f"Файл не найден: {e}")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")

    def admin_panel_callback(self, message):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Add Test Case", callback_data="add_test_case")
        keyboard.add(button)
        self.bot.send_message(message.chat.id, "Admin Panel", reply_markup=keyboard)

    def handle_callback_query(self, call):
        if call.data == "add_test_case":
            self.bot.send_message(call.message.chat.id, "Adding a test case...")

    def process_priority_id(self, message):
        priority_id = message.text
        self.bot.send_message(message.chat.id, "Введите текст для тестового кейса:")
        self.bot.register_next_step_handler(message, self.process_text, priority_id)

    def process_text(self, message, priority_id):
        text = message.text
        self.add_test_case(priority_id, text)
        self.bot.send_message(message.chat.id, f"Тестовый кейс успешно добавлен с priority_id: {priority_id}, текстом: {text}")

    def process_title(self, message):
        title = message.text
        self.bot.send_message(message.chat.id, "Введите URL для ссылки:")
        self.bot.register_next_step_handler(message, self.process_url, title)

    def process_url(self, message, title):
        url = message.text
        self.add_data(title, url, "links")
        self.bot.send_message(message.chat.id, f"Ссылка успешно добавлена с title: {title}, URL: {url}")