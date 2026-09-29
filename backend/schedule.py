from flask import Blueprint, request, jsonify
from memberSystem.schedule import (
    insert_data,
    get_schedule_and_trips_by_user_id,
    select_by_user_id,
    select_by_id,
    update_schedule,
    delete_schedule
)
from memberSystem.trip import (
    insert_trip,
    select_trip_by_user_id,
    select_trip_by_id,
    update_trip,
    delete_trip,
    update_time,
    reflow_schedule
)
from tools.distanceNtime import getDistanceNtime
from datetime import datetime
import json
sch_bp = Blueprint('sch', __name__)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M")
        return super().default(o)


# 新增行程表 API
@sch_bp.route('/api/schedule/insert_data', methods=['POST'])
def route_insert_data():
    data = request.get_json()
    result, message = insert_data(**data)

    if result:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 201


# 取得行程表(含子行程) API
@sch_bp.route('/api/schedule/getScheduleNTrips/<user_id>', methods=['GET'])
def route_get_schedule_and_trips(user_id):
    result, data = get_schedule_and_trips_by_user_id(user_id)

    if result:
        return jsonify(data), 200
    else:
        return jsonify({'message': data}), 401


# 以使用者ID取得行程表(不含子行程) API
@sch_bp.route('/api/schedule/select_by_user_id/<user_id>', methods=['GET'])
def route_select_by_user_id(user_id):
    result, data = select_by_user_id(user_id)

    if result:
        return jsonify(data), 200
    else:
        return jsonify({'message': data}), 401


# 以行程表ID取得行程表 API
@sch_bp.route('/api/schedule/select_by_id/<schedule_id>', methods=['GET'])
def route_select_by_id(schedule_id):
    result, data = select_by_id(schedule_id)

    if result:
        return jsonify(data), 200
    else:
        return jsonify({'message': data}), 401


# 更新行程表 API
@sch_bp.route('/api/schedule/update_schedule/<event_id>', methods=['PUT'])
def route_update_schedule(event_id):
    data = request.get_json()
    print(data)

    new_name = data.get('name')
    new_description = data.get('sDescribe')
    new_start_date = data.get('startDate')
    new_end_date = data.get('endDate')
    new_privilege = data.get('privilege')

    result, message = update_schedule(event_id, new_name, new_start_date, new_end_date, new_description, new_privilege)

    if result:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 401


# 刪除行程表 API
@sch_bp.route('/api/schedule/delete_schedule/<event_id>', methods=['DELETE'])
def route_delete_schedule(event_id):
    result, message = delete_schedule(event_id)

    if result:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 401


# 新增行程 API
@sch_bp.route('/api/trips', methods=['POST'])
def add_trip():
    data = request.json
    scheduleID = data.get('scheduleID')
    trip_type = data.get('trip_type')
    trip_id = data.get('trip_id')
    user_id = data.get('user_id')
    success, message = insert_trip(
        scheduleID,
        trip_type,
        trip_id,
        user_id
    )

    if success:
        return jsonify({'success': True, 'message': message}), 201
    else:
        return jsonify({'success': False, 'message': message}), 401


# 取得使用者所有行程 API
@sch_bp.route('/api/trips/user/<int:user_id>', methods=['GET'])
def get_user_trips(user_id):
    success, trips = select_trip_by_user_id(user_id)

    if success:
        return jsonify({'success': True, 'trips': trips}), 200
    else:
        return jsonify({'success': False, 'message': trips}), 401


# 取得單一行程 API
@sch_bp.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip_details(trip_id):
    success, trip_details = select_trip_by_id(trip_id)

    if success:
        return jsonify({'success': True, 'tripDetails': trip_details}), 200
    else:
        return jsonify({'success': False, 'message': trip_details}), 500


# 更新行程 API
@sch_bp.route('/api/trips/<int:trip_id>', methods=['PUT'])
def update_trip_route(trip_id):
    data = request.json
    new_scheduleID = data.get('new_scheduleID')
    new_type = data.get('new_type')
    new_trip = data.get('new_trip')
    new_start_date = data.get('new_start_date')
    new_end_date = data.get('new_end_date')
    new_user_id = data.get('new_user_id')
    success, message = update_trip(
        new_scheduleID,
        trip_id,
        new_type,
        new_trip,
        new_start_date,
        new_end_date,
        new_user_id
    )

    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 500


# 更新行程時間 API
@sch_bp.route('/api/trips/<int:trip_id>/update_time', methods=['PUT'])
def update_trip_time(trip_id):
    data = request.json
    print(data)
    new_start_date = data.get('new_start_date')
    durationHour = data.get('durationHour')
    durationMinute = data.get('durationMinute')

    success, message = update_time(
        trip_id,
        new_start_date,
        durationHour,
        durationMinute
    )

    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 500


# 刪除行程 API
@sch_bp.route('/api/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip_route(trip_id):
    success, message = delete_trip(trip_id)

    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 500


# 依新順序重排行程時間 API（拖曳排序後呼叫）
# body: {"order": [{"tripID": 12, "day": 1}, ...]}
@sch_bp.route('/api/schedule/<int:schedule_id>/reflow', methods=['POST'])
def reflow_schedule_route(schedule_id):
    data = request.get_json() or {}
    success, message = reflow_schedule(schedule_id, data.get('order', []))

    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400


# 取得距離與時間 API
@sch_bp.route('/api/get_distance_and_time', methods=['POST'])
def get_distance_and_time():
    data = request.get_json()
    aID = data.get('aID')
    aType = data.get('aType')
    aTrip = data.get('aTrip')
    bID = data.get('bID')
    bType = data.get('bType')
    bTrip = data.get('bTrip')
    end_date = data.get('end_date')
    b_durationH = data.get('b_durationH')
    b_drurationM = data.get('b_drurationM')

    success, distance_and_time = getDistanceNtime(
        aID,
        aType,
        aTrip,
        bID,
        bType,
        bTrip,
        end_date,
        b_durationH,
        b_drurationM,
    )

    if success:
        return json.dumps(distance_and_time, cls=DateTimeEncoder, ensure_ascii=False), 200
    else:
        return jsonify({'success': False, 'message': distance_and_time}), 500
