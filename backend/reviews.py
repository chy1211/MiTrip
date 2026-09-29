from flask import Blueprint, request, jsonify
from gettingData.reviews.RestaurantReviews import (
    getRestReviews,
    addRestReview,
    updateRestReview,
    deleteRestReview,
    getRestReviewsByUserId
)
from gettingData.reviews.HotelReviews import (
    addHotelReview,
    getHotelReviews,
    getHotelReviewsByUserId,
    updateHotelReview,
    deleteHotelReview
)
from gettingData.reviews.AttractionReviews import (
    addAttractionReview,
    getAttractionReviews,
    getAttractionReviewsByUserId,
    updateAttractionReview,
    deleteAttractionReview
)


rev_bp = Blueprint('rev', __name__)


# 取得餐廳評論 (依照餐廳ID)
@rev_bp.route('/api/restaurant/<restaurantsId>/reviews', methods=['GET'])
def getRestaurantReviews(restaurantsId):
    data = getRestReviews(restaurantsId)
    return jsonify(data)


# 取得餐廳評論（依照使用者ID）
@rev_bp.route('/api/restaurant/userID/<userId>/reviews', methods=['GET'])
def getRestaurantReviewsByUserID(userId):
    reviews = getRestReviewsByUserId(userId)
    return jsonify({'reviews': reviews}), 200


# 新增餐廳評論
@rev_bp.route('/api/restaurant/addReview', methods=['POST'])
def addRestaurantReview():
    data = request.get_json()
    restaurant_id = data.get('restaurantId')
    user_id = data.get('userId')
    text = data.get('text')
    user_rating = data.get('userRating')
    print(restaurant_id, user_id, text, user_rating)

    addRestReview(restaurant_id, user_id, text, user_rating)

    return jsonify({'message': 'Review added successfully'}), 201


# 修改餐廳評論
@rev_bp.route('/api/restaurant/updateReview', methods=['PUT'])
def updateRestaurantReview():
    data = request.get_json()
    text_id = data.get('textId')
    new_text = data.get('newText')
    new_user_rating = data.get('newUserRating')

    updateRestReview(text_id, new_text, new_user_rating)

    return jsonify({'message': 'Review updated successfully'}), 200


# 刪除餐廳評論
@rev_bp.route('/api/restaurant/deleteReview', methods=['DELETE'])
def deleteRestaurantReviews():
    text_id = request.args.get('textId')

    if text_id is None:
        return jsonify({'message': 'Missing request parameters'}), 400

    deleteRestReview(text_id)

    return jsonify({'message': 'Review deleted successfully'}), 200


# 新增飯店評論
@rev_bp.route('/api/hotel/addReview', methods=['POST'])
def addHotelReviewRoute():
    data = request.get_json()
    hotel_id = data.get('hotelId')
    user_id = data.get('userId')
    text = data.get('text')
    user_rating = data.get('userRating')

    addHotelReview(hotel_id, user_id, text, user_rating)

    return jsonify({'message': 'Review added successfully'}), 201


# 取得飯店評論 (依照飯店ID)
@rev_bp.route('/api/hotel/<hotelId>/reviews', methods=['GET'])
def getHotelReviewsRoute(hotelId):
    data = getHotelReviews(hotelId)
    return jsonify(data)


# 取得飯店評論（依照使用者ID）
@rev_bp.route('/api/hotel/userID/<userId>/reviews', methods=['GET'])
def getHotelReviewsByUserIdRoute(userId):
    reviews = getHotelReviewsByUserId(userId)
    return jsonify({'reviews': reviews}), 200


# 修改飯店評論
@rev_bp.route('/api/hotel/updateReview', methods=['PUT'])
def updateHotelReviewRoute():
    data = request.get_json()
    text_id = data.get('textId')
    new_text = data.get('newText')
    new_user_rating = data.get('newUserRating')

    updateHotelReview(text_id, new_text, new_user_rating)

    return jsonify({'message': 'Review updated successfully'}), 200


# 刪除飯店評論
@rev_bp.route('/api/hotel/deleteReview', methods=['DELETE'])
def deleteHotelReviewRoute():
    text_id = request.args.get('textId')

    if text_id is None:
        return jsonify({'message': 'Missing request parameters'}), 400

    deleteHotelReview(text_id)

    return jsonify({'message': 'Review deleted successfully'}), 200


# 新增景點評論
@rev_bp.route('/api/attraction/addReview', methods=['POST'])
def addAttractionReviewRoute():
    data = request.get_json()
    attraction_id = data.get('attractionId')
    user_id = data.get('userId')
    text = data.get('text')
    user_rating = data.get('userRating')

    addAttractionReview(attraction_id, user_id, text, user_rating)

    return jsonify({'message': 'Review added successfully'}), 201


# 取得景點評論 (依照景點ID)
@rev_bp.route('/api/attraction/<attractionId>/reviews', methods=['GET'])
def getAttractionReviewsRoute(attractionId):
    reviews = getAttractionReviews(attractionId)
    return jsonify({'reviews': reviews}), 200


# 取得景點評論（依照使用者ID）
@rev_bp.route('/api/attraction/userID/<userId>/reviews', methods=['GET'])
def getAttractionReviewsByUserIdRoute(userId):
    reviews = getAttractionReviewsByUserId(userId)
    return jsonify({'reviews': reviews}), 200


# 修改景點評論
@rev_bp.route('/api/attraction/updateReview', methods=['PUT'])
def updateAttractionReviewRoute():
    data = request.get_json()
    text_id = data.get('textId')
    new_text = data.get('newText')
    new_user_rating = data.get('newUserRating')

    if text_id is None or new_text is None or new_user_rating is None:
        return jsonify({'message': 'Missing parameters in request body'}), 400

    updateAttractionReview(text_id, new_text, new_user_rating)

    return jsonify({'message': 'Review updated successfully'}), 200


# 刪除景點評論
@rev_bp.route('/api/attraction/deleteReview', methods=['DELETE'])
def deleteAttractionReviewRoute():
    text_id = request.args.get('textId')

    if text_id is None:
        return jsonify({'message': 'Missing request parameters'}), 400

    deleteAttractionReview(text_id)

    return jsonify({'message': 'Review deleted successfully'}), 200
