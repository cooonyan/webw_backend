import os
from flask import Blueprint, request, jsonify
import sqlite3, bcrypt, jwt, datetime
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

bp = Blueprint('login', __name__)

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@bp.route('/login', methods=['POST'])
def login():
    try:
        conn = sqlite3.connect('userdata.db')
        if not request.is_json:
            print(request, "1")
            return jsonify({'status': 'fail','message':'잘못된 요청입니다.'}), 400
        data = request.get_json()
        username = data.get('username')
        private_token = data.get('private_token')
        if not username or not private_token:
            print(request, "2")
            return jsonify({'status': 'fail','message':'잘못된 요청입니다 (요청값이 비었습니다.)'}), 400

        cursor = conn.cursor()
        cursor.execute('SELECT private_token FROM "userINFO" WHERE userName = ?', (username,))
        row = cursor.fetchone()
        
        if row is None or not bcrypt.checkpw(private_token.encode('utf-8'), row[0]):
            return jsonify({'status': 'fail','message':'아이디 혹은 비밀번호가 틀립니다.'}), 401
        conn.close()
        token = generate_token(username)
        return jsonify({'status': 'cool', 'message': '로그인 성공', 'token': token}), 200

    except Exception as e:
        print(e)
        return jsonify({'status': 'fail','message':'unknown request'}), 500

    finally:
        if conn:
            conn.close()
