import React, { useEffect } from "react";
import { View, Text, TouchableOpacity, Image, StyleSheet, SafeAreaView, StatusBar } from 'react-native';
import {createDrawerNavigator} from '@react-navigation/drawer';
import HomeScreen from "../screens/HomeScreen";
import RecommendationsScreen from '../screens/RecommendationsScreen';
import ItineraryScreen from '../screens/ItineraryScreen';
import Tabs, { getHeaderTitle } from "./tabs";
import { DrawerContent } from "../screens/DrawerContent";
import ProfileStackScreen from "../screens/ProfileStackScreen";
import EditProfileScreen from "../screens/EditProfileScreen";
import { Entypo as IconE, Ionicons as Icon } from '@expo/vector-icons';
import unmountOnBlur from './unmountOnBlur';

const TabsScreen = unmountOnBlur(Tabs);


const Drawer = createDrawerNavigator();

const MyDrawers = ({navigation}) => {


    return (
        <Drawer.Navigator drawerContent={props => <DrawerContent {... props} />}
            screenOptions={({ route }) => ({
                headerStyle: {
                    backgroundColor: 'white',
                },
                headerTitleStyle: {
                    fontSize: 25,
                    fontWeight: 'bold',
                    color: 'black',
                },
                headerTitleAlign:'center',
                headerTintColor: '#7ed957',
                
            })}
            
            
            >

            {/* <Drawer.Screen name="設定" component={ProfileScreen}  /> */}
            <Drawer.Screen name="tabs" component={TabsScreen} options={({ route }) => ({ title: '首頁', headerTitle: getHeaderTitle(route) })} />
            <Drawer.Screen name="Home" component={HomeScreen} options={{title: '首頁'}} />
            <Drawer.Screen name="Recommendations" component={RecommendationsScreen} options={{title: '推薦'}} />
            <Drawer.Screen name="Itinerary" component={ItineraryScreen} options={{title: '行程'}} />
            <Drawer.Screen name="ProfileStack" component={ProfileStackScreen} options={{title: '個人'}} />
            <Drawer.Screen name="EditProfileScreen" component={EditProfileScreen} 
                options={({navigation}) => ({
                    title: '推薦',
                    headerLeft: () => (
                        <Icon.Button name="arrow-undo"size={25}backgroundColor={"#fff"}color={"#000"}onPress={() => navigation.goBack()}/>
                    )
                })} 
            />

            

            
        </Drawer.Navigator>
    );
}
export default MyDrawers;




const styless = StyleSheet.create({
    tabcontainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 12,
        paddingVertical: 5,
        backgroundColor: 'white',
    },
});