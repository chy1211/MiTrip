// Backend base URL. Set EXPO_PUBLIC_API_URL in front/.env, e.g.
//   EXPO_PUBLIC_API_URL=http://192.168.1.10:5000
// (use the LAN IP of the machine running the backend so a phone/iPad can reach it)
export const API_BASE_URL = (process.env.EXPO_PUBLIC_API_URL || 'http://localhost:5000').replace(/\/+$/, '');
