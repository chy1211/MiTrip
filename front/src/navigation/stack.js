import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import {Button}  from 'react-native';
import HomeScreen from "../screens/HomeScreen";
import ProfileScreen from "../screens/ProfileScreen";
import Tabs from "./tabs";
const ProfileStack = createStackNavigator();


const ProfileStackScreen11 = ({navigation}) => {
    return(
        <ProfileStack.Navigator screenOptions={{
            headerStyle:{
                backgroundColor:'#fff',
            },
            headerTintColor:'#000',
            headerTitleStyle:{
                fontWeight:'bold',
            },
        }}
        >
            
            <ProfileStack.Screen
                name='Profile'
                component={ProfileScreen}
                options={{
                    title:'',
            }}
            />
            <ProfileStack.Screen
                name='Tabs'
                component={Tabs}
                options={{
                    title:'',
            }}
            />
        </ProfileStack.Navigator>

    )
}
export default ProfileStackScreen11;