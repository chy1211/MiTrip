import React , {useState} from "react";
import {SafeAreaView, View, Text, TextInput, TouchableOpacity, StyleSheet, Alert} from 'react-native';
import { API_BASE_URL } from '../constants/config';

const fetchData =  async (option,username1,password1,checkPassword1,email1,birthDay1,restaurantid,userid,text,userRating,Token,placeType='restaurant') => {

    const errorResponse = { success: false, error: '請輸入帳號和密碼' };
    console.log(option,username1,password1,checkPassword1,email1,birthDay1);

    const checkTemp = (temp,word) => {
        if (temp !== '') {
            temp += '、';
        }
        temp += word;
        return temp;
        };


const showAlert = (title,word) => {
    Alert.alert(
        title,
        word,
        [
            { text: '確定', onPress: () => console.log('確定按鈕被按下！') }
        ],
        { cancelable: true }
    );
};
        //判斷 登入/註冊/忘記密碼
    switch (option) {
        case 'Login':
            
            try {

                // 檢查 email 和 password 是否存在
                if (!username1 || !password1 ) {
                    let temp = '';
                    
                    !username1 && (temp += '帳號');
                    !password1 && (temp = checkTemp(temp,'密碼'));

                    errorResponse.error = temp+'不得為空';

                    return errorResponse;
                }


                const response = await fetch(`${API_BASE_URL}/api/login`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                    username: username1,
                    password: password1,

                    }),
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // 假設伺服器端返回 JSON 格式的回應
                const responseData = await response.json();

                // 在這裡處理從伺服器獲取的回應
                console.log('Login successful:', responseData);
                if (responseData == "Registration successful") {
                    showAlert('恭喜!','登入成功!');
                }
                return { success: true, data: responseData };
                // 可以在這裡進行導航或其他操作
                } catch (error) {
                console.error('Error during login:', error);
                return { success: false, error: 'An error occurred during login.' };
                }

            break;
            case 'userInfo':
            
            try {

                // 檢查 email 和 password 是否存在
                if (!Token ) {

                    errorResponse.error = 'Token為空';

                    return errorResponse;
                }


                const response = await fetch(`${API_BASE_URL}/api/user-information`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        token: Token

                    }),
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // 假設伺服器端返回 JSON 格式的回應
                const responseData = await response.json();

                // 在這裡處理從伺服器獲取的回應
                return { success: true, data: responseData };
                // 可以在這裡進行導航或其他操作
                } catch (error) {
                console.error('Error during login:', error);
                return { success: false, error: 'An error occurred during login.' };
                }

            break;
            case 'Logout':
            
            try {
                // 檢查 email 和 password 是否存在
                if (!Token) {
                    errorResponse.error = 'Token不存在';
                    return errorResponse;
                }


                const response = await fetch(`${API_BASE_URL}/api/logout`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        token:Token
                    }),
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // 假設伺服器端返回 JSON 格式的回應
                const responseData = await response.json();

                // 在這裡處理從伺服器獲取的回應
                console.log('Logout successful:', responseData);
                
                return { success: true, data: responseData };
                // 可以在這裡進行導航或其他操作
                } catch (error) {
                console.error('Error during logout:', error);
                return { success: false, error: 'An error occurred during logout.' };
                }

            break;

        case 'Register':

            try {

                // 檢查 email 和 password 是否存在
                if (!username1 || !password1 || !email1 || !birthDay1 || !checkPassword1) {
                    let temp = '';
                    
                    !username1 && (temp += '帳號');
                    !password1 && (temp = checkTemp(temp,'密碼'));
                    !email1 && (temp = checkTemp(temp,'電子信箱'));
                    !birthDay1 && (temp = checkTemp(temp,'生日'));
                    !checkPassword1 && (temp = checkTemp(temp,'確認密碼'));

                    showAlert('提示',temp+'不得為空');
                    return { success: false };
                }

                //判斷密碼和檢查密碼是否相同
                if (checkPassword1 != password1) {
                    showAlert('提示','密碼須和重複密碼一致');
                    return { success: false };
                }
                const response = await fetch(`${API_BASE_URL}/api/register`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                    username: username1,
                    password: password1,
                    email: email1,
                    birthDay: birthDay1,

                    }),
                });
                
                if (!response.ok) {
                    const failure = await response.json().catch(() => ({}));
                    return { success: false, error: failure.message === 'Username already exists' ? '此帳號已被註冊' : '註冊失敗，請稍後再試' };
                }

                // 假設伺服器端返回 JSON 格式的回應
                const responseData = await response.json();

                // 在這裡處理從伺服器獲取的回應
                console.log('Login successful:', responseData);
                
                return { success: true, data: responseData };
                
                // 可以在這裡進行導航或其他操作
                } catch (error) {
                console.error('Error during login:', error);
                return { success: false, error: '連線發生錯誤，請稍後再試' };
                }
            
            break;
        case 'ForgetPassword':

            try {

                // 檢查 username 和 email 是否存在
                if (!username1 || !email1 ) {
                    let temp = '';
                    
                    !username1 && (temp += '帳號');
                    !email1 && (temp = checkTemp(temp,'信箱'));

                    showAlert('提示',temp+'不得為空');
                    return { success: false };
                }


                const response = await fetch(`${API_BASE_URL}/api/validate-user`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                    username: username1,
                    email: email1,

                    }),
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // 假設伺服器端返回 JSON 格式的回應
                const responseData = await response.json();

                // 在這裡處理從伺服器獲取的回應
                console.log('message:', responseData);
                // if (responseData == "Registration successful") {
                //     showAlert('恭喜!','驗證成功!');
                //     // 返回一個包含結果的對象
                //     return { success: true, data: responseData };
                // }
                return { success: true, data: responseData };
                
                // 可以在這裡進行導航或其他操作
                } catch (error) {
                console.error('Error during login:', error);
                // 返回一個包含錯誤信息的對象
                return { success: false, error: 'An error occurred during fetch.' };
                }
            
                
            break;
            case 'UpdatePassword':

            try {

                // 檢查 password 和 checkPassword 是否存在
                if (!password1 || !checkPassword1) {
                    let temp = '';
                    !password1 && (temp = checkTemp(temp,'密碼'));
                    !checkPassword1 && (temp = checkTemp(temp,'確認密碼'));

                    showAlert('提示',temp+'不得為空');
                    return { success: false };
                }

                //判斷密碼和檢查密碼是否相同
                if (checkPassword1 != password1) {
                    showAlert('提示','密碼須和重複密碼一致');
                    return { success: false };
                }
                const response = await fetch(`${API_BASE_URL}/api/reset-password`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                    username: username1,
                    newPassword: password1,
                    }),
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // 假設伺服器端返回 JSON 格式的回應
                const responseData = await response.json();

                // 在這裡處理從伺服器獲取的回應
                console.log('Login successful:', responseData);
                
                showAlert('恭喜!','更改成功!');
                return { success: true, data: responseData };
                // 可以在這裡進行導航或其他操作
                } catch (error) {
                console.error('Error during login:', error);
                return { success: false, error: '連線發生錯誤，請稍後再試' };
                }
            
            break;

            case 'PostComment':
            try {
                // 檢查其他參數是否存在
                if (!restaurantid || !userid || !text || !userRating) {
                    // 處理參數不正確的情況
                    showAlert('提示', '請提供完整的評論資訊');
                    return { success: false };
                }

                // 處理其他相關的評論提交邏輯
                const response = await fetch(`${API_BASE_URL}/api/${placeType}/addReview`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        [{ restaurant: 'restaurantId', attraction: 'attractionId', hotel: 'hotelId' }[placeType]]: restaurantid,
                        userId: userid,
                        text: text,
                        userRating: userRating,
                    }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // 假設伺服器端返回 JSON 格式的回應
                const responseData = await response.json();

                // 在這裡處理從伺服器獲取的回應
                console.log('Comment posted successfully:', responseData);

                showAlert('提示', '評論提交成功');
                return { success: true, data: responseData };
                // 可以在這裡進行導航或其他操作
            } catch (error) {
                console.error('Error during comment posting:', error);
                showAlert('錯誤', '評論提交失敗');
                return { success: false, error: error.message };
            }

        default:
            break;
    }
}




export default fetchData