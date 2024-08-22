from flask import request, Blueprint, jsonify, current_app
from module.login import verify_token
import sqlite3

bp = Blueprint('edit_service', __name__)

def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@bp.route('/edit_service', methods=['POST'])
def edit_service():
    try:
        if not request.is_json:
            return jsonify({'status': 'fail','message':'bad request'}), 400
        data = request.get_json()
        token = request.headers.get('Authorization').split(' ')[1]  # Extract token from Authorization header
        username = verify_token(token)
        if username is None:
            return jsonify({'status': 'fail','message':'만료된 토큰'}), 401
        owner = username
        service_name = data.get('service_name')
        service_label = data.get('service_label')
        service_url = data.get('service_url')
        activate = data.get('activate')
        user_link1 = data.get('user_link1')
        user_link2 = data.get('user_link2')
        user_link3 = data.get('user_link3')
        user_link1_name = data.get('user_link1_name')
        user_link2_name = data.get('user_link2_name')
        user_link3_name = data.get('user_link3_name')
        conn = sqlite3.connect('userdata.db')
        cursor = conn.cursor()

        print(f"Checking for duplicate service URL: {service_url} for owner: {owner}")
        cursor.execute('SELECT * FROM userService WHERE service_url = ? AND owner != ?', (service_url, owner))
        duplicate_service = cursor.fetchone()
        print("Duplicate service check result:", duplicate_service)
        if service_url == '' : pass
        else:
            if duplicate_service is not None:
                return jsonify({'status': 'fail', 'message': '이미 사용 중인 서비스 URL입니다.'}), 409

        cursor.execute('SELECT * FROM userService WHERE owner = ?', (username,))
        user_service = cursor.fetchone()

        cursor.execute('SELECT * FROM userService WHERE owner = ?', (username,))
        user_service = cursor.fetchone()
        if user_service is None:
            print("요청 찾기 불가")
            print(user_service)
            return jsonify({'status': 'fail','message':'요청자를 찾을 수 없음'}), 401
        else:
            cursor.execute('UPDATE userService SET service_name = ?, service_label = ?, service_url = ?, activate = ?, user_link1 = ?, user_link2 = ?, user_link3 = ?, user_link1_name = ?, user_link2_name = ?, user_link3_name = ? WHERE owner = ?',
                           (service_name, service_label, service_url, activate, user_link1, user_link2, user_link3, user_link1_name, user_link2_name, user_link3_name, username))
        conn.commit()
        conn.close()
        print("서비스 업데이트 성공")
        print(service_name, service_label, service_url, activate, user_link1, user_link2, user_link3, user_link1_name, user_link2_name, user_link3_name)
        return jsonify({'status': 'success','message':'서비스가 성공적으로 업데이트 됨'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail','message':'unknown request'}), 500