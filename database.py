import os
import psycopg
from psycopg.rows import dict_row

# Получение переменных окружения
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def init_db():
    """
    Инициализация базы данных.
    Создает таблицу users, если она еще не существует.
    """
    try:
        # Подключение к базе данных
        with psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            # Создание курсора
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        total_money INT DEFAULT 0,
                        click_power INT DEFAULT 1,
                        money_per_click INT DEFAULT 1,
                        click_count INT DEFAULT 0
                    )
                ''')
        print("База данных инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")

def get_user_data(user_id):
    """
    Получение данных пользователя по его ID.
    Возвращает словарь с данными пользователя или None, если пользователь не найден.
    """
    try:
        with psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                row = cursor.fetchone()
                return row
    except Exception as e:
        print(f"Ошибка при получении данных пользователя: {e}")
        return None

def update_user_data(user_id, total_money, click_power, money_per_click, click_count):
    """
    Обновление данных пользователя.
    Если пользователь не существует, создает новую запись.
    """
    try:
        with psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO users (user_id, total_money, click_power, money_per_click, click_count)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET
                        total_money = EXCLUDED.total_money,
                        click_power = EXCLUDED.click_power,
                        money_per_click = EXCLUDED.money_per_click,
                        click_count = EXCLUDED.click_count
                ''', (user_id, total_money, click_power, money_per_click, click_count))
        print(f"Данные пользователя {user_id} обновлены.")
    except Exception as e:
        print(f"Ошибка при обновлении данных пользователя: {e}")

# Точка входа для тестирования
if __name__ == "__main__":
    # Инициализация базы данных
    init_db()

    # Пример использования функций
    user_id = 123456789
    total_money = 100
    click_power = 2
    money_per_click = 1
    click_count = 50

    # Обновление данных пользователя
    update_user_data(user_id, total_money, click_power, money_per_click, click_count)

    # Получение данных пользователя
    user_data = get_user_data(user_id)
    if user_data:
        print(f"Данные пользователя: {user_data}")
    else:
        print("Пользователь не найден.")