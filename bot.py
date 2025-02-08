import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

SERVER_URL = "https://piranhaclickerbot.onrender.com"  
# SERVER_URL = "https://your-render-url.onrender.com"  # На Render

# Токен бота (замените на ваш токен)
TOKEN = "7693663885:AAFMIqw6_x69OjAhBhYLKqOeyqKpD2MEBtE"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Используйте команды для взаимодействия.")

# Обработка кликов
async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = {
        "user_id": str(user_id),
        "data": {
            "totalMoney": 100,  # Пример данных
            "clickPower": 1,
            "moneyPerClick": 1,
            "clickCount": 10
        }
    }

    # Отправка данных на сервер
    url = f"{SERVER_URL}/save-progress"
    response = requests.post(url, json=data)
    print("Ответ сервера:", response.status_code, response.text)  # Логирование ответа

    if response.status_code == 200:
        await update.message.reply_text("Прогресс сохранен!")
    else:
        await update.message.reply_text("Ошибка при сохранении прогресса.")

# Основная функция
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_click))

    # Запуск бота
    print("Бот запущен. Нажмите Ctrl + C для остановки.")
    application.run_polling()

if __name__ == "__main__":
    main()