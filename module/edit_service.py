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
            return jsonify({'status': 'fail','message':'invalid or expired token'}), 401

        owner = data.get('owner')
        service_name = data.get('service_name')
        service_label = data.get('service_label')
        service_url = data.get('service_url')
        activate = data.get('activate')

        conn = sqlite3.connect('userdata.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM userService WHERE owner = ?', (owner,))
        user_service = cursor.fetchone()

        if user_service is None:
            return jsonify({'status': 'fail','message':'owner not found'}), 401
        else:
            cursor.execute('UPDATE userService SET service_name = ?, service_label = ?, service_url = ?, activate = ? WHERE owner = ?', 
                           (service_name, service_label, service_url, activate, owner))

        conn.commit()
        conn.close()

        return jsonify({'status': 'success','message':'service updated successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail','message':'unknown request'}), 500