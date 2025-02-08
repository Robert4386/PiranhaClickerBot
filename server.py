from flask import Flask, request, jsonify
from database import get_user_data, update_user_data

app = Flask(__name__)

@app.route('/get-user-data', methods=['POST'])
def get_user_data_route():
    data = request.json
    user_id = data.get('user_id')
    user_data = get_user_data(user_id)
    if user_data:
        return jsonify(user_data)
    return jsonify({})

@app.route('/save-progress', methods=['POST'])
def save_progress_route():
    data = request.json
    user_id = data['user_id']
    total_money = data['data']['totalMoney']
    click_power = data['data']['clickPower']
    money_per_click = data['data']['moneyPerClick']
    click_count = data['data']['clickCount']
    update_user_data(user_id, total_money, click_power, money_per_click, click_count)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    from database import init_db
    init_db()  # Инициализация базы данных
    app.run(debug=True)