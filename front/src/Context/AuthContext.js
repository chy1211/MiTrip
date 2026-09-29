import React, {Children, createContext, useState, useEffect, } from "react";
import {Alert} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import fetchData from "../components/fetchData";

export const AuthContext = createContext();

export const AuthProvider = ({children}) => {
    const [isLoading, setIsLoading] = useState(false); //讀取動畫
    const [userToken, setUserToken] = useState(null);
    const [username, setUsername] = useState(null);
    const [userID, setUserID] = useState(0);
    const [email, SetEmail] = useState('');
    const [birthDay, SetBirthDay] = useState('');

        //登入動作
    const login = async(option, username, password) => {
        setIsLoading(true);
        
        const response = await fetchData(option='Login',
                    username,
                    password
                );

        if (response.success) {
            //設置TOKEN=
            setUserToken(response.data.token);
            setUsername(username);
            AsyncStorage.setItem('userToken', response.data.token );
            AsyncStorage.setItem('username', username );

            let tempToken = response.data.token;
            //抓取UserID
            const userInfo = async(tempToken) => {
                const response = await fetchData(option='userInfo',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    tempToken
                        );
                console.log(tempToken,'temptoken');
                console.log('response',response);
                if (response.success) {
                    //設置userID
                    let temp = JSON.stringify(response.data.info.user_id);
                    setUserID(temp);
                    AsyncStorage.setItem('userID', temp );
                    let email =JSON.stringify(response.data.info.email);
                    let newEmail = email.replace(/"/g, '');
                    let birthDay =JSON.stringify(response.data.info.birthDay);
                    let newBirthDay =birthDay.replace(/"/g, '');
                    //轉換成字串並儲存
                    console.log('email',newEmail);
                    console.log('birthDay',newBirthDay);
                    SetEmail(newEmail);
                    AsyncStorage.setItem('email', newEmail );
                    SetBirthDay(newBirthDay);
                    AsyncStorage.setItem('birthDay', newBirthDay );
                    return('success');

                } else {
                    // 如果有錯誤，顯示錯誤信息或者進行其他處理
                    if (response.error) {
                        Alert.alert('Error', response.error);
                        return('error');
                    } else {
                        // 如果錯誤信息不存在，顯示一般性錯誤提示
                        Alert.alert('Error', 'An error occurred during catching userinfo.');
                        return('error');
                    }
                }
    
            }
            userInfo(tempToken);


        } else {
            // 如果有錯誤，顯示錯誤信息或者進行其他處理
            if (response.error) {
                Alert.alert('Error', response.error);
                setIsLoading(false);
                return('error');
            } else {
                // 如果錯誤信息不存在，顯示一般性錯誤提示
                Alert.alert('Error', 'An error occurred during login.');
                setIsLoading(false);
                return('error');
            }
        }

        setIsLoading(false);
    }

    ///登出
    const logout = async() => {
        setIsLoading(true);

        const response = await fetchData('Logout',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
                    userToken
                );

        if (response.success) {
            //設置TOKEN
            console.log('Logout Success');
            setUserToken(null);
            AsyncStorage.removeItem('userToken');
            setUsername(null);
            AsyncStorage.removeItem('username');
            setUserID(0);
            AsyncStorage.removeItem('userID');
            SetEmail('');
            AsyncStorage.removeItem('email');
            SetBirthDay(null);
            AsyncStorage.removeItem('birthDay');
            
            setIsLoading(false);
        } else {
            // 如果有錯誤，顯示錯誤信息或者進行其他處理
            if (response.error) {
                Alert.alert('Error', response.error);
            } else {
                // 如果錯誤信息不存在，顯示一般性錯誤提示
                Alert.alert('Error', 'An error occurred during login.');
                setIsLoading(false);
            }
        }

        setIsLoading(false);
    }
    

    //確認登入
    const isLoggedIn = async() =>{
        try{
            setIsLoading(true);
            let userToken = await AsyncStorage.getItem('userToken');
            let username = await AsyncStorage.getItem('username');
            let userID = await AsyncStorage.getItem('userID');
            let birthDay = await AsyncStorage.getItem('birthDay');
            let email = await AsyncStorage.getItem('email');
            setUserToken(userToken);
            setUsername(username);
            setUserID(userID);
            SetBirthDay(birthDay);
            SetEmail(email);
            setIsLoading(false);
        } catch(e) {
            console.log('isLoggedIn:\n');
            console.log(`isLogged in error ${e}`);
        }  
        

    }

    useEffect(() => {
        isLoggedIn();
        }, []);

    return(
        <AuthContext.Provider value={{login, logout, isLoading, isLoggedIn, userToken,username,userID,email,birthDay}}>
            {children}
        </AuthContext.Provider>

    )
}