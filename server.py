from flask import Flask, request, jsonify
from database import get_user_data, update_user_data

app = Flask(__name__)

# Маршрут для проверки работоспособности сервера
@app.route('/')
def home():
    return "Server is running!"

# Маршрут для получения данных пользователя
@app.route('/get-user-data', methods=['POST'])
def get_user_data_route():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user_data = get_user_data(user_id)
    if user_data:
        return jsonify(user_data)
    return jsonify({})

# Маршрут для сохранения прогресса пользователя
@app.route('/save-progress', methods=['POST'])
def save_progress_route():
    data = request.json
    user_id = data.get('user_id')
    total_money = data['data'].get('totalMoney')
    click_power = data['data'].get('clickPower')
    money_per_click = data['data'].get('moneyPerClick')
    click_count = data['data'].get('clickCount')

    if not all([user_id, total_money, click_power, money_per_click, click_count]):
        return jsonify({"error": "Missing required fields"}), 400

    update_user_data(user_id, total_money, click_power, money_per_click, click_count)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    from database import init_db
    init_db()  # Инициализация базы данных
    app.run(debug=True)