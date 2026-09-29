import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid

# 連接 MySQL 資料庫
from config import MYSQL_CONFIG as mysql_config


def register_user(username, password, email, birth_day):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # 檢查是否已經存在相同的使用者名稱
        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return False, 'Username already exists'

        # 創建新使用者
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO User (username, password, email, birthDay) VALUES (%s, %s, %s, %s)",
                       (username, hashed_password, email, birth_day))
        conn.commit()
        conn.close()

        return True, 'Registration successful'
    except Exception as e:
        return False, str(e)


def login_user(username, password):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        # 檢查使用者是否存在並檢驗密碼
        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            # 生成驗證令牌
            token_id = str(uuid.uuid4())
            expiration_time = datetime.now() + timedelta(days=1)  # 令牌有效期為一天
            cursor.execute("INSERT INTO Token (user_id, token, expiration_time) VALUES (%s, %s, %s)",
                           (user[0], token_id, expiration_time))
            conn.commit()
            conn.close()
            return token_id
        else:
            return None
    except Exception as e:
        return None


def logout_user(token_id):
    try:
        # 使驗證令牌失效
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Token WHERE token = %s", (token_id,))
        conn.commit()
        conn.close()
        return True, 'Logout successful'
    except Exception as e:
        return False, str(e)


def check_authentication(token_id):
    try:
        # 檢查驗證令牌是否有效
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Token WHERE token = %s AND expiration_time > NOW()", (token_id,))
        token = cursor.fetchone()
        if token:
            conn.close()
            return True, 'Authentication successful'
        else:
            conn.close()
            return False, 'Invalid token'
    except Exception as e:
        return False, str(e)


def change_password(username, old_password, new_password):
    try:
        # 檢查使用者是否存在並檢驗密碼
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], old_password):
            # 更新密碼
            hashed_new_password = generate_password_hash(new_password)
            cursor.execute("UPDATE User SET password = %s WHERE username = %s", (hashed_new_password, username))
            conn.commit()
            conn.close()
            return True, 'Password changed successfully'
        else:
            conn.close()
            return False, 'Invalid credentials'
    except Exception as e:
        return False, str(e)


def validate_user(username, email):
    try:
        # 檢查使用者是否存在並檢驗電子郵件
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = %s AND email = %s", (username, email))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except Exception as e:
        return False


def reset_password(username, new_password):
    try:
        # 檢查使用者是否存在
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            # 更新使用者密碼
            hashed_password = generate_password_hash(new_password)
            cursor.execute("UPDATE User SET password = %s WHERE username = %s",
                           (hashed_password, username))
            conn.commit()
            conn.close()
            return True, 'Password reset successful'
        else:
            conn.close()
            return False, 'User not found'
    except Exception as e:
        return False, str(e)


def get_UserInfo(token):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM Token WHERE token = %s", (token,))
        user = cursor.fetchone()
        user_id = user[0]
        cursor.execute("SELECT * FROM User WHERE id = %s", (user_id,))
        userInfo = cursor.fetchone()
        cursor.execute("SELECT * FROM Token WHERE token = %s AND expiration_time > NOW()", (token,))
        token = cursor.fetchone()
        parsed_date = datetime.strptime(str(userInfo[4]), "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        if token:
            returnData = {
                "user_id": user_id,
                "username": userInfo[1],
                "email": userInfo[3],
                "birthDay": formatted_date
            }
            conn.close()
            return True, returnData, "Authentication successful"
        else:
            conn.close()
            returnData = {
                "user_id": user_id,
                "username": userInfo[1],
                "email": userInfo[3],
                "birthDay": formatted_date
            }
            return True, returnData, "Token expired"
    except Exception as e:
        return False, None, str(e)
