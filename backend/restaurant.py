from flask import Blueprint, request, jsonify
from gettingData.getRestaurantRecommended import getRestRec
from gettingData.getRestaurantDetail import getRestDetail
from gettingData.getRestaurantSearch import getRestSearch

res_bp = Blueprint('res', __name__)


# 取得餐廳推薦 API
@res_bp.route('/api/restaurant', methods=['GET'])
def getRestaurantsRecommended():
    user_id = request.args.get('user_id')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    last = request.args.get('last')

    if user_id == '0' and last is not None:
        data = getRestRec(user_id, float(lat), float(lng), int(last))
    else:
        data = getRestRec(user_id, float(lat), float(lng))

    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Not Found'}), 404


# 取得餐廳詳細資訊 API
@res_bp.route('/api/restaurant/<restaurantsId>', methods=['GET'])
def getRestaurantDetail(restaurantsId):
    user_id = request.args.get('user_id')
    data = getRestDetail(user_id, restaurantsId)
    return jsonify(data), 200


# 取得餐廳搜尋 API
@res_bp.route('/api/restaurant/search', methods=['GET'])
def searchRestaurant():
    keyWord = request.args.get('keyWord')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    data = getRestSearch(keyWord, lng, lat)
    return jsonify(data), 200
