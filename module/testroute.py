from flask import Blueprint, request, jsonify

bp = Blueprint('testroute', __name__)

@bp.route('/test', methods=['POST'])
def test():
    try:
        if request.is_json:
            data = request.get_json() 
        else:
            return jsonify({'status': 'fail','message':'bad request'}), 400

        getdata = data.get('testdata', 'default_value')
        print(f"we get {getdata} from client")
        afterdata = {'status': 'cool', 'data': getdata}
        return jsonify(afterdata)  
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail','message':'unknown request'}), 500
