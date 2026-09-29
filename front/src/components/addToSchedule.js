import { Alert } from 'react-native';
import { API_BASE_URL } from '../constants/config';

// Ask which of the user's itineraries a place should be added to, then POST it to /api/trips.
// tripType: 'Restaurant' | 'Attraction' | 'Hotel' (the type names stored in the trip table)
export async function addToSchedule({ userID, tripType, tripId }) {
    if (!userID) {
        Alert.alert('新增到行程', '請先登入');
        return;
    }
    let schedules = {};
    try {
        const response = await fetch(`${API_BASE_URL}/api/schedule/select_by_user_id/${userID}`);
        schedules = await response.json();
    } catch (error) {
        console.error(error);
    }
    const options = Object.values(schedules || {}).map(schedule => ({
        text: schedule.name,
        onPress: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/trips`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        scheduleID: schedule.scheduleID,
                        trip_type: tripType,
                        trip_id: tripId,
                        user_id: userID,
                    }),
                });
                if (!response.ok) {
                    throw new Error('HTTP error ' + response.status);
                }
                Alert.alert('成功', '已成功新增到行程');
            } catch (error) {
                console.error(error);
                Alert.alert('錯誤', '新增到行程失敗');
            }
        },
    }));
    if (options.length === 0) {
        Alert.alert('新增到行程', '目前還沒有行程，請先到「行程」新增一個行程');
        return;
    }
    options.push({ text: '取消', style: 'cancel' });
    Alert.alert('新增到行程', '請選擇要新增到哪一個行程', options, { cancelable: true });
}

// DetailScreen receives the lower-case API type ('restaurant'); trips store 'Restaurant'.
export const tripTypeOf = (dataType) => (dataType ? dataType.charAt(0).toUpperCase() + dataType.slice(1) : 'Restaurant');
