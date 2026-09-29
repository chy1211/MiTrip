from flask import Blueprint, request, jsonify
from memberSystem.userAuth import (
    register_user,
    login_user,
    logout_user,
    check_authentication,
    change_password,
    validate_user,
    reset_password,
    get_UserInfo
)

auth_bp = Blueprint('auth', __name__)


# 註冊 API
@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    birth_day = data.get('birthDay')
    result, message = register_user(username, password, email, birth_day)
    print(result, message)

    if result:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'message': message}), 400


# 登入 API
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    token = login_user(username, password)

    if token:
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# 登出 API
@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    token_id = request.headers.get('Authorization')

    result, message = logout_user(token_id)

    if result:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 401


# 檢查驗證狀態 API
@auth_bp.route('/api/check-auth', methods=['GET'])
def check_auth():
    token_id = request.headers.get('Authorization')

    result, message = check_authentication(token_id)

    if result:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 401


# 修改密碼 API
@auth_bp.route('/api/change-password', methods=['POST'])
def change_password_api():
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    success, message = change_password(username, old_password, new_password)

    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 401


# 驗證使用者(重設密碼)
@auth_bp.route('/api/validate-user', methods=['POST'])
def validate_user_api():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    valid_user = validate_user(username, email)

    if valid_user:
        return jsonify({'message': 'User validation successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or email'}), 400


# 重設密碼
@auth_bp.route('/api/reset-password', methods=['POST'])
def reset_password_api():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('newPassword')

    success, message = reset_password(username, new_password)

    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400


# UserInformation API
@auth_bp.route('/api/user-information', methods=['POST'])
def get_user_information():
    data = request.get_json()
    token = data.get('token')
    success, info, expired = get_UserInfo(token)
    if success and expired == "Authentication successful":
        return jsonify({'message': 'User validation successful', 'info': info}), 200
    elif success and expired == "Token expired":
        return jsonify({'message': 'Token expired', 'info': info}), 400
    else:
        return jsonify({'message': 'Invalid token'}), 400
