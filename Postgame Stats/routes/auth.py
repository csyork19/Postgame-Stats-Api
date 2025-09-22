import sqlite3
import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

# ⚠️ Move this to a config file / env var in production
SECRET_KEY = "my_dirty_little_secret"

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, hashed_password)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()

    if row and check_password_hash(row[0], password):
        token = jwt.encode(
            {
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401
