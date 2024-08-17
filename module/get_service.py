from flask import Blueprint, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
from module.login import verify_token

bp = Blueprint('get_service', __name__)
CORS(bp)

@bp.route('/get_service', methods=['POST'])
def get_service():
    try:
        print(request)
        if not request.is_json:
            return jsonify({'status': 'fail', 'message': '잘못된 형식'}), 400
        
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return jsonify({'status': 'fail', 'message': 'Authorization header 누락'}), 401
        
        token = auth_header.split(' ')[1]  
        username = verify_token(token)
        if username is None:
            return jsonify({'status': 'fail', 'message': '잘못되거나 만료된 토큰'}), 401

        with sqlite3.connect('userdata.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM userService WHERE owner = ?', (username,))
            user_service = cursor.fetchone()

            if user_service is None:
                return jsonify({'status': 'fail', 'message': '서비스 조회 불가'}), 403

            return jsonify({'status': 'success', 'service': {
                'service_owner': user_service[0],
                'service_name': user_service[1],
                'service_label': user_service[2],
                'service_url': user_service[3],
                'activate': user_service[4],
                'user_link1': user_service[5],
                'user_link2': user_service[6],
                'user_link3': user_service[7],
                'user_link1_name': user_service[8],
                'user_link2_name': user_service[9],
                'user_link3_name': user_service[10]
            }}), 200
    
    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'message': 'DB에러', 'error': str(e)}), 500
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'fail', 'message': '토큰 만료됨'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'fail', 'message': '잘못된 토큰'}), 401
    except Exception as e:
        return jsonify({'status': 'fail', 'message': 'Unknown error', 'error': str(e)}), 500
