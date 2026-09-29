import React, {useContext} from "react";
import {View,Text, ActivityIndicator} from 'react-native';
import { createStackNavigator } from "@react-navigation/stack";
import { NavigationContainer } from "@react-navigation/native";

import AuthStack from "./auth";
import AppNavigator from ".";
import { AuthContext } from "../Context/AuthContext";
import { StatusBar } from "expo-status-bar";

const AppNav = () => {
    const {isLoading, userToken} = useContext(AuthContext);

    if (isLoading) {
        return(
            <View style={{flex:1, justifyContent:'center', alignContent:'center',}}>
                <ActivityIndicator size={'large'} />
            </View>
        );
    }
    return(
        // navigationInChildEnabled keeps the React Navigation 6 behaviour of navigate() reaching screens in nested navigators
        <NavigationContainer navigationInChildEnabled>
            <StatusBar style="auto" />
                {/* { userToken !== null 
                ? <AppNavigator />
                : <AuthStack />
        } */}
            <AppNavigator />
        </NavigationContainer>
    )


}


export default AppNav