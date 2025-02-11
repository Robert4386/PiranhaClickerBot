import os
import asyncio
import asyncpg

# Получение переменных окружения
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

async def init_db():
    """
    Инициализация базы данных.
    Создает таблицу users, если она еще не существует.
    """
    try:
        # Подключение к базе данных
        conn = await asyncpg.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        # Создание таблицы
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                total_money INT DEFAULT 0,
                click_power INT DEFAULT 1,
                money_per_click INT DEFAULT 1,
                click_count INT DEFAULT 0
            )
        ''')
        print("База данных инициализирована.")
        await conn.close()
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")

async def get_user_data(user_id):
    """
    Получение данных пользователя по его ID.
    Возвращает словарь с данными пользователя или None, если пользователь не найден.
    """
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        row = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
        await conn.close()
        return dict(row) if row else None
    except Exception as e:
        print(f"Ошибка при получении данных пользователя: {e}")
        return None

async def update_user_data(user_id, total_money, click_power, money_per_click, click_count):
    """
    Обновление данных пользователя.
    Если пользователь не существует, создает новую запись.
    """
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        await conn.execute('''
            INSERT INTO users (user_id, total_money, click_power, money_per_click, click_count)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_id) DO UPDATE SET
                total_money = EXCLUDED.total_money,
                click_power = EXCLUDED.click_power,
                money_per_click = EXCLUDED.money_per_click,
                click_count = EXCLUDED.click_count
        ''', user_id, total_money, click_power, money_per_click, click_count)
        print(f"Данные пользователя {user_id} обновлены.")
        await conn.close()
    except Exception as e:
        print(f"Ошибка при обновлении данных пользователя: {e}")

# Точка входа для тестирования
if __name__ == "__main__":
    # Запуск асинхронного цикла
    async def main():
        await init_db()

        # Пример использования функций
        user_id = 123456789
        total_money = 100
        click_power = 2
        money_per_click = 1
        click_count = 50

        # Обновление данных пользователя
        await update_user_data(user_id, total_money, click_power, money_per_click, click_count)

        # Получение данных пользователя
        user_data = await get_user_data(user_id)
        if user_data:
            print(f"Данные пользователя: {user_data}")
        else:
            print("Пользователь не найден.")

    asyncio.run(main())