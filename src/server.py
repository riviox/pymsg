from flask import Flask, request, jsonify
import json

app = Flask(__name__)

users_file = 'users.json'
messages = []

def load_users():
    try:
        with open(users_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

users = load_users()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username in users and users[username] == password:
        return jsonify({'status': f'Logged in as {username}'})
    else:
        return jsonify({'status': 'Invalid username or password'}), 401

@app.route('/send', methods=['POST'])
def send_message():
    username = request.json.get('username')
    message = request.json.get('message')
    if username not in users:
        return jsonify({'status': 'User not logged in'}), 401
    messages.append({'username': username, 'message': message})
    return jsonify({'status': 'Message received'})

@app.route('/receive', methods=['GET'])
def receive_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
