from flask import Blueprint, request, jsonify
from datetime import datetime
import json
from collections import OrderedDict
from gettingData.getExploreInfo import (
    checkHottestHistory,
    checkHottestCity,
    checkHottestSchedule,
    likeSchedule,
    getNews
)

exp_bp = Blueprint('exp', __name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


# 檢查熱門歷史
@exp_bp.route('/api/explore/checkHottestHistory', methods=['GET'])
def checkHottestHistoryRoute():
    success, data = checkHottestHistory()

    if success:
        return jsonify({'success': True, 'data': data}), 200
    else:
        return jsonify({'success': False, 'message': data}), 500


# 檢查熱門城市
@exp_bp.route('/api/explore/checkHottestCity', methods=['GET'])
def checkHottestCityRoute():
    success, data = checkHottestCity()

    ordered_data = OrderedDict(
            sorted(
                data.items(),
                key=lambda x: x[1]['values'],
                reverse=True
            )
        )

    # print(ordered_data)
    if success:
        return json.dumps(
                {
                    'success': True,
                    'data': dict(ordered_data)
                }
            ), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        return jsonify({'success': False, 'message': data}), 500


# 檢查熱門行程表
@exp_bp.route('/api/explore/checkHottestSchedule', methods=['GET'])
def checkHottestScheduleRoute():
    user_id = request.args.get('user_id')
    success, data = checkHottestSchedule(user_id)

    ordered_data = OrderedDict(
        sorted(
            data.items(),
            key=lambda x: x[1]['numberofLikes'],
            reverse=True
        )
    )

    if success:
        return json.dumps(
            {
                'success': True,
                'data': dict(ordered_data)
            },
            default=json_serial  # 指定自定義序列化方法
        ), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        return jsonify({'success': False, 'message': data}), 500


# 按讚行程表
@exp_bp.route('/api/explore/likeSchedule', methods=['GET'])
def likeScheduleRoute():
    user_id = request.args.get('user_id')
    schedule_id = request.args.get('schedule_id')
    success, data = likeSchedule(user_id, schedule_id)

    if success:
        return jsonify({'success': True, 'data': data}), 200
    else:
        return jsonify({'success': False, 'message': data}), 500


# 檢查最新消息
@exp_bp.route('/api/explore/get_news', methods=['GET'])
def api_get_news():
    success, data = getNews()
    if success:
        return jsonify(
            {
                "success": True,
                "data": data
            }
        ), 200
    else:
        return jsonify(
            {
                "success": False,
                "data": data
            }
        ), 500
