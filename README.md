# Бот-помощник в обучении технического администратора

## Описание

Этот бот предназначен для обучения технического администратора процессам дежурства. Есть возможность прорешать тестовые кейсы для отработки определения приоритета задачи, можно воспользоваться шаблоном коммуникации, а так же получить полезные для дежурного ресурсы.

## Структура проекта
- `main.py`: Основной файл запуска бота.

- Bot
  - `main_bot.py`: Логика основного функционала бота.

  -  `admin_bot.py`: Логика админ-панели.

  -  `keyboards.py`: Создание клавиатур.

- Database 
  - `database.py`: Управление базой данных.

- Config
  - `config.json`: Конфигурационный файл.

- Servicies Директория с JSON-файлами данных.

## Структура базы данных

![Схема БД](Servicies\res\db.png)

### Таблица `users`
- **id**: SERIAL PRIMARY KEY
- **user_id**: INTEGER UNIQUE NOT NULL
- **username**: VARCHAR(255) NOT NULL
- **first_name**: VARCHAR(255)
- **last_name**: VARCHAR(255)
- **is_admin**: BOOLEAN DEFAULT FALSE

### Таблица `admins`
- **id**: SERIAL PRIMARY KEY
- **user_id**: INTEGER UNIQUE NOT NULL REFERENCES users(user_id)
- **admin_nickname**: VARCHAR(255) NOT NULL

### Таблица `test_cases`
- **id**: SERIAL PRIMARY KEY
- **number**: INTEGER NOT NULL
- **priority_id**: INTEGER UNIQUE NOT NULL REFERENCES priority(priority_id)

### Таблица `test_case_results`
- **id**: SERIAL PRIMARY KEY
- **user_id**: INTEGER NOT NULL REFERENCES users(user_id)
- **test_case_id**: INTEGER NOT NULL REFERENCES test_cases(id)
- **is_correct**: BOOLEAN NOT NULL
- **timestamp**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Таблица `priority`
- **priority_id**: SERIAL PRIMARY KEY
- **priority_name**: VARCHAR(15) NOT NULL

## Функциональность

### Основные команды

- `/start`: Приветственное сообщение и регистрация пользователя.
- `/useful_links`: Полезные ссылки и ресурсы.
- `/create_communication`: Создание коммуникаций.
- `/test_cases`: Прохождение тестовых кейсов.
- `/admin_panel`: Панель администратора для управления данными.

### Обработчики сообщений

- Обработка текстовых сообщений для вывода клавиатур с ссылками.
- Обработка callback-запросов для управления тестовыми кейсами и коммуникациями.

### Админ-панель

- Добавление и удаление тестовых кейсов.
- Загрузка файлов.
- Управление данными.

