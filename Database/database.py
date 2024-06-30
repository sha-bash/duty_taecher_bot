import json
import psycopg2
from Config.config import read_json

class DatabaseManager:
    
    @staticmethod
    def get_connection():
        config_path = 'Config/config.json'
        config = read_json(config_path)

        return psycopg2.connect(dbname=config['database']['dbname'],
                                user=config['database']['user'],
                                password=config['database']['password'],
                                host=config['database']['host'], 
                                port=config['database']['port'])
    
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
                number VARCHAR(255) NOT NULL,
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
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)

    def add_user(self, user_id, username, first_name, last_name, is_admin=False):
        sql = """INSERT INTO users(user_id, username, first_name, last_name, is_admin)
                 VALUES(%s, %s, %s, %s, %s) RETURNING id;"""
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (user_id, username, first_name, last_name, is_admin))
                new_user_id = cur.fetchone()[0]
                conn.commit()  
                return new_user_id
        
    def add_test_case(self, number, priority_id):
        sql = """INSERT INTO test_cases(number, priority_id)
                 VALUES(%s, %s) RETURNING id;"""
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (number, priority_id))
                test_case_id = cur.fetchone()[0]
                conn.commit()  
                return test_case_id

    def load_data_from_json(self, json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        for item in data:
            number = item['number']
            priority_id = item['priority_id'] 
            self.add_test_case(number, priority_id)
    
    def add_ptiority(self):
        sql = """
            INSERT INTO priority(priority_name) 
            SELECT * FROM (VALUES ('Молния'), ('Высокий'), ('Средний'), ('Низкий')) AS data(priority_name)
            WHERE NOT EXISTS (SELECT 1 FROM priority WHERE priority.priority_name = data.priority_name)
            RETURNING priority_id;
            """
    
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                inserted_ids = cur.fetchone()
                conn.commit()
                return [inserted_id[0] for inserted_id in inserted_ids]

    def get_priorities(self):
        sql = """
            SELECT priority_name FROM priority;
            """
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                priority_names = cur.fetchall()  
                conn.commit()
                return [priority[0] for priority in priority_names]  


