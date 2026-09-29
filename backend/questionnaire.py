from flask import Blueprint, request, jsonify
from memberSystem.qes import addRecord, ifRecord

qes_bp = Blueprint('qes', __name__)


# 新增問卷紀錄
@qes_bp.route('/api/qes/addRecord', methods=['POST'])
def qesAddRecord():
    data = request.get_json()
    success, message = addRecord(data)
    if success:
        return jsonify({'message': "addRecord successful"}), 200
    elif message == 'isRecord.':
        return jsonify({'message': message}), 409
    else:
        return jsonify({'message': 'Error'}), 500


# 是否已填寫問卷
@qes_bp.route('/api/qes/isRecord/<userID>', methods=['GET'])
def qesIsRecord(userID):
    isRecord = ifRecord(userID)
    if isRecord:
        return jsonify({'message': "isRecord."}), 200
    else:
        return jsonify({'message': 'is not Record.'}), 201
