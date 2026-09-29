import React from "react";
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import ProfileScreen from "./ProfileScreen";
import Icon from '@expo/vector-icons/MaterialCommunityIcons'
import EditProfileScreen from './EditProfileScreen'

const ProfileStack = createNativeStackNavigator();


const ProfileStackScreen = ({navigation}) => {
    return(
        <ProfileStack.Navigator screenOptions={{
            // headerStyle:{
            //     backgroundColor:'#fff',
            // },
            // headerTintColor:'#000',
            // headerTitleStyle:{
            //     fontWeight:'bold',
            // },
            headerShown:false,
        }}
        >
            
            <ProfileStack.Screen
                name='Profile'
                component={ProfileScreen}
            //     options={{
            //         title:'',
            //         headerRight: () => (
            //             <Icon.Button 
            //                 name="account-edit"
            //                 size={25}
            //                 backgroundColor={"#fff"}
            //                 color={"#000"}
            //                 onPress={() => navigation.navigate('EditProfile')}
            //             />
            //         )
            // }}
            />
                <ProfileStack.Screen 
                    name='EditProfile'
                    component={EditProfileScreen}
                />
        </ProfileStack.Navigator>

    )
}
export default ProfileStackScreen;