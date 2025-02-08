import os
import psycopg2
from psycopg2.extras import DictCursor

# Получение переменных окружения
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def init_db():
    """Инициализация базы данных."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                total_money INT DEFAULT 0,
                click_power INT DEFAULT 1,
                money_per_click INT DEFAULT 1,
                click_count INT DEFAULT 0
            )
        ''')
        conn.commit()
        print("База данных инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_user_data(user_id):
    """Получение данных пользователя."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"Ошибка при получении данных пользователя: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def update_user_data(user_id, total_money, click_power, money_per_click, click_count):
    """Обновление данных пользователя."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, total_money, click_power, money_per_click, click_count)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                total_money = EXCLUDED.total_money,
                click_power = EXCLUDED.click_power,
                money_per_click = EXCLUDED.money_per_click,
                click_count = EXCLUDED.click_count
        ''', (user_id, total_money, click_power, money_per_click, click_count))
        conn.commit()
        print(f"Данные пользователя {user_id} обновлены.")
    except Exception as e:
        print(f"Ошибка при обновлении данных пользователя: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()