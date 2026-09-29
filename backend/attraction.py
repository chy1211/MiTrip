from flask import Blueprint, request, jsonify
from gettingData.getAttractionRecommended import getAttractionRec
from gettingData.getAttractionDetail import getAttractionDetail
from gettingData.getAttractionSearch import getAttractionSearch

attr_bp = Blueprint('attr', __name__)


# 取得景點推薦 API
@attr_bp.route('/api/attraction', methods=['GET'])
def getAttractionsRecommended():
    user_id = request.args.get('user_id')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    last = request.args.get('last')

    if user_id == '0' and last is not None:
        data = getAttractionRec(user_id, float(lat), float(lng), int(last))
    else:
        data = getAttractionRec(user_id, float(lat), float(lng))

    if data is not None:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Not Found'}), 404


# 取得景點詳細資訊 API
@attr_bp.route('/api/attraction/<attractionId>', methods=['GET'])
def getAttractionDetailRoute(attractionId):
    user_id = request.args.get('user_id')
    data = getAttractionDetail(user_id, attractionId)
    return jsonify(data), 200


# 取得景點搜尋 API
@attr_bp.route('/api/attraction/search', methods=['GET'])
def searchAttraction():
    keyWord = request.args.get('keyWord')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    data = getAttractionSearch(keyWord, lng, lat)
    return jsonify(data), 200
