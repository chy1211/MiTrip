import React from 'react';
import { Polyline } from 'react-native-maps';

// One colour per day; day 1 uses the app's green.
const DAY_COLORS = ['#7ed957', '#4a90e2', '#f5a623', '#e4533a', '#9b59b6', '#1abc9c'];

const hasPosition = (trip) => trip.lat != null && trip.lng != null;

// Straight lines between consecutive stops of the same day. `trips` come from
// /api/schedule/select_by_id (without the "Days" separators), already ordered by day and start time.
export function TripRouteLines({ trips }) {
    const days = {};
    trips.filter(hasPosition).forEach((trip) => {
        (days[trip.onDay] = days[trip.onDay] || []).push({ latitude: Number(trip.lat), longitude: Number(trip.lng) });
    });
    return Object.keys(days)
        .filter((day) => days[day].length > 1)
        .map((day) => (
            <Polyline
                key={`day-${day}`}
                coordinates={days[day]}
                strokeColor={DAY_COLORS[(Number(day) - 1) % DAY_COLORS.length]}
                strokeWidth={4}
            />
        ));
}

// "1小時20分" / "35分" / "小於1分"; null when the travel time has not been computed yet.
// (The 2023 cards only showed the minutes, so a 1h20m drive was displayed as "20分".)
export function formatTravelTime(hours, minutes) {
    if (hours == null && minutes == null) {
        return null;
    }
    const total = (Number(hours) || 0) * 60 + (Number(minutes) || 0);
    if (total === 0) {
        return '小於1分';
    }
    const h = Math.floor(total / 60);
    const m = total % 60;
    if (h === 0) {
        return `${m}分`;
    }
    return m === 0 ? `${h}小時` : `${h}小時${m}分`;
}

// Initial map region that shows every stop (instead of zooming in on the first one only).
export function regionForTrips(trips) {
    const points = trips.filter(hasPosition);
    if (points.length === 0) {
        return undefined;
    }
    const lats = points.map((t) => Number(t.lat));
    const lngs = points.map((t) => Number(t.lng));
    const minLat = Math.min(...lats), maxLat = Math.max(...lats);
    const minLng = Math.min(...lngs), maxLng = Math.max(...lngs);
    return {
        latitude: (minLat + maxLat) / 2,
        longitude: (minLng + maxLng) / 2,
        latitudeDelta: Math.max(0.01, (maxLat - minLat) * 1.5),
        longitudeDelta: Math.max(0.01, (maxLng - minLng) * 1.5),
    };
}
