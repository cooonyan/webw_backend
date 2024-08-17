import sqlite3
from flask import Blueprint, request, jsonify



bp = Blueprint('service', __name__)

def get_db_connection():
    conn = sqlite3.connect('userdata.db')
    conn.row_factory = sqlite3.Row
    return conn

@bp.route('/service', methods=['POST'])
def get_service():
    data = request.get_json()
    service_url = data.get('service_url')
    if not service_url:
        return jsonify({'status': 'fail', 'message': '나쁜 요청'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT service_name, service_label, activate FROM userService WHERE service_url = ?', (service_url,))
    service = cursor.fetchone()
    conn.close()

    if service is None:
        return jsonify({'status': 'fail', 'message': '404 페이지로 이동'}), 405
    
    if service['activate'] == 0:
        return jsonify({'status': 'middleman', 'message': '비활성화된 페이지 404로 이동'}), 405
    else:
        return jsonify({'status': 'success', 'service': {
            'service_name': service['service_name'],
            'service_label': service['service_label']
        }}), 200
    
    

