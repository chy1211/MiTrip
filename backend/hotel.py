from flask import Blueprint, request, jsonify
from gettingData.getHotelRecommended import getHotelRec
from gettingData.getHotelDetail import getHotelDetail
from gettingData.getHotelSearch import getHotelSearch

hot_bp = Blueprint('hot', __name__)


# 取得餐廳推薦 API
@hot_bp.route('/api/hotel', methods=['GET'])
def getHotelsRecommended():
    user_id = request.args.get('user_id')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    last = request.args.get('last')

    if user_id == '0' and last is not None:
        data = getHotelRec(user_id, float(lat), float(lng), int(last))
    else:
        data = getHotelRec(user_id, float(lat), float(lng))

    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Not Found'}), 404


# 取得餐廳詳細資訊 API
@hot_bp.route('/api/hotel/<hotelsId>', methods=['GET'])
def route_GetHotelDetail(hotelsId):
    user_id = request.args.get('user_id')
    data = getHotelDetail(user_id, hotelsId)
    return jsonify(data), 200


# 取得餐廳搜尋 API
@hot_bp.route('/api/hotel/search', methods=['GET'])
def searchHotel():
    keyWord = request.args.get('keyWord')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    data = getHotelSearch(keyWord, lng, lat)
    return jsonify(data), 200
