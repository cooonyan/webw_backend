from flask import request, Blueprint, jsonify
import sqlite3, bcrypt

def username_check(username):
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "userINFO" WHERE userName = ?', (username,))
    if cursor.fetchone() == None:
        conn.close()
        return False
    conn.close()
    return True

bp = Blueprint('register', __name__)

@bp.route('/register', methods=['POST'])
def register():
    try:
        if not request.is_json:
            return jsonify({'status': 'fail','message':'메소드 나쁜 요청'}), 400
        data = request.get_json()
        username = data.get('username')
        private_token = data.get('private_token')
        if not username or not private_token:
            return jsonify({'status': 'fail','message':'나쁜 요청'}), 400
        conn = sqlite3.connect('userdata.db')
        cursor = conn.cursor()
        if username_check(username):
            conn.close()
            return jsonify({'status': 'fail','message':'사용자가 이미 존재한'}), 400
        hashed_token = bcrypt.hashpw(private_token.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            'INSERT INTO "userInfo" (userName, private_token) VALUES (?, ?)',
            (username, hashed_token))
        cursor.execute(
            'INSERT INTO "userService" (owner, service_name, service_label, service_url, activate, user_link1, user_link2, user_link3, user_link1_name, user_link2_name, user_link3_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (username, '', '', '', False, '', '', '', '', '', ''))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success','message':'가입 성공'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail','message':str(e)}), 500
    finally:
        try:
            if conn:
                conn.close()
        except:
            pass

