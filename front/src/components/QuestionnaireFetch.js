import React , {useState} from "react";
import {SafeAreaView, View, Text, TextInput, TouchableOpacity, StyleSheet, Alert} from 'react-native';
import { API_BASE_URL } from '../constants/config';

const QuestionnairefetchData =  async (
    Age,
    Gender,
    Job,
    TravelDays,
    TravelDaysBudget1,
    TravelDaysBudget2,
    TravelDaysBudget3,
    TravelDaysBudget5,
    TravelDaysBudget7,
    TravelType,
    TravelSchedule,
    TravelPeople,
    MtTravelType,
    CityTravelDays,
    PurchasedItem,
    TravelInfo,
    TravelNeeds,
    TravelMedia,
    userID,
) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/qes/addRecord`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                Age:Age,
                Gender:Gender,
                Job:Job,
                TravelDays:TravelDays,
                TravelDaysBudget1:TravelDaysBudget1,
                TravelDaysBudget2:TravelDaysBudget2,
                TravelDaysBudget3:TravelDaysBudget3,
                TravelDaysBudget5:TravelDaysBudget5,
                TravelDaysBudget7:TravelDaysBudget7,
                TravelType:TravelType,
                TravelSchedule:TravelSchedule,
                TravelPeople:TravelPeople,
                MtTravelType:MtTravelType,
                CityTravelDays:CityTravelDays,
                PurchasedItem:PurchasedItem,
                TravelInfo:TravelInfo,
                TravelNeeds:TravelNeeds,
                TravelMedia:TravelMedia,
                userID:userID,
            }),
        });
        
        if (!response.ok) {
            const failure = await response.json().catch(() => ({}));
            return { success: false, error: failure.message === 'isRecord.' ? '您已經填寫過問卷' : '繳交時發生錯誤' };
        }

        // 假設伺服器端返回 JSON 格式的回應
        const responseData = await response.json();

        // 在這裡處理從伺服器獲取的回應
        console.log('addRecord', responseData);
        if (responseData.message == "addRecord successful") {
            return { success: true, data: responseData.message };
        } else {
            return { success: false, error: responseData.message };
        }
        } catch (error) {
            console.error('Error during login:', error);
            return { success: false, error: '繳交時發生錯誤' };
        }

}

export default QuestionnairefetchData