import json
import psycopg2
from Config.config import read_json

class DatabaseManager:
    
    @staticmethod
    def get_connection():
        config_path = 'Config/config.json'
        config = read_json(config_path)
        return psycopg2.connect(
            dbname=config['database']['dbname'],
            user=config['database']['user'],
            password=config['database']['password'],
            host=config['database']['host'], 
            port=config['database']['port']
        )
    
    def __init__(self):
        self.connection = DatabaseManager.get_connection()
    
    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                username VARCHAR(255) NOT NULL,
                first_name  VARCHAR(255),
                last_name  VARCHAR(255),
                is_admin BOOLEAN DEFAULT FALSE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS admins (
                id SERIAL PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL REFERENCES users(user_id),
                admin_nickname VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS test_cases (
                id SERIAL PRIMARY KEY,
                number INTEGER NOT NULL,
                priority_id INTEGER UNIQUE NOT NULL REFERENCES priority(priority_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS test_case_results (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id),
                test_case_id INTEGER NOT NULL REFERENCES test_cases(id),
                is_correct BOOLEAN NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS priority (
                priority_id serial PRIMARY KEY,
                priority_name varchar(15) not null
            )
            """
        )
        with self.connection.cursor() as cur:
            for command in commands:
                cur.execute(command)
            self.connection.commit()

    def add_user(self, user_id, username, first_name, last_name, is_admin=False):
        sql = """INSERT INTO users(user_id, username, first_name, last_name, is_admin)
                 VALUES(%s, %s, %s, %s, %s) RETURNING id;"""
        with self.connection.cursor() as cur:
            cur.execute(sql, (user_id, username, first_name, last_name, is_admin))
            new_user_id = cur.fetchone()[0]
            self.connection.commit()  
            return new_user_id
        
    def add_test_case(self, number, priority_id):
        sql = """INSERT INTO test_cases(number, priority_id)
                 VALUES(%s, %s) RETURNING id;"""
        with self.connection.cursor() as cur:
            try:
                cur.execute(sql, (number, priority_id))
                test_case_id = cur.fetchone()[0]
                self.connection.commit()
                return test_case_id
            except psycopg2.IntegrityError as e:
                self.connection.rollback()
                if 'duplicate key value violates unique constraint "test_cases_priority_id_key"' in str(e):
                    print(f"Запись с priority_id={priority_id} уже существует. Пропускаем добавление.")
                else:
                    raise e

    def load_data_from_json(self, json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        cases = data.get('cases', [])
        for item in cases:
            number = item.get('number')
            priority_id = item.get('priority_id')
            if not self.check_priority_exists(priority_id):
                test_case_id = self.add_test_case(number, priority_id)
                if test_case_id is None:
                    print(f"Тестовый кейс с number={number}, priority_id={priority_id} не был добавлен.")

    def check_priority_exists(self, priority_id):
        sql = "SELECT COUNT(*) FROM priority WHERE priority_id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (priority_id,))
            count = cur.fetchone()[0]
            return count > 0

    def add_priority(self):
        sql = """
            INSERT INTO priority(priority_name) 
            SELECT * FROM (VALUES ('Молния'), ('Высокий'), ('Средний'), ('Низкий')) AS data(priority_name)
            WHERE NOT EXISTS (SELECT 1 FROM priority WHERE priority.priority_name = data.priority_name)
            RETURNING priority_id;
            """
        with self.connection.cursor() as cur:
            cur.execute(sql)
            inserted_ids = cur.fetchall()
            self.connection.commit()
            return [inserted_id[0] for inserted_id in inserted_ids]

    def get_priorities(self):
        sql = """
            SELECT priority_name FROM priority;
            """
        with self.connection.cursor() as cur:
            cur.execute(sql)
            priority_names = cur.fetchall()  
            return [priority[0] for priority in priority_names]
    
    def record_test_case_result(self, user_id, test_case_id, is_correct):
        sql = """
            INSERT INTO test_case_results (user_id, test_case_id, is_correct)
            VALUES (%s, %s, %s)
        """
        with self.connection.cursor() as cur:
            cur.execute(sql, (user_id, test_case_id, is_correct))
            self.connection.commit()