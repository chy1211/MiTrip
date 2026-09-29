import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { View, Text, TouchableOpacity, Image, StyleSheet, SafeAreaView, StatusBar } from 'react-native';
import HomeScreen from '../screens/HomeScreen';
import RecommendationsScreen from '../screens/RecommendationsScreen';
import ItineraryScreen from '../screens/ItineraryScreen';
import { styles } from '../screens/styles';
import Iconf from '@expo/vector-icons/FontAwesome';
import { MaterialIcons as Iconm, AntDesign as Icona } from '@expo/vector-icons'; 
import ProfileScreen from '../screens/ProfileScreen';
import { useNavigation } from '@react-navigation/native';
import { getFocusedRouteNameFromRoute } from '@react-navigation/native';
import ProfileStackScreen from '../screens/ProfileStackScreen';
import SocialScreen from '../screens/SocialScreen';
import unmountOnBlur from './unmountOnBlur';

const RecommendationsTab = unmountOnBlur(RecommendationsScreen);
const ItineraryTab = unmountOnBlur(ItineraryScreen);

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const ProfileStack = createStackNavigator();

// const CustomHeader = ({ title }) => (
//     <SafeAreaView style={{backgroundColor: "white", paddingVertical:20}}>  
//         <StatusBar backgroundColor="white" barStyle="dark-content" />
//         <View style={[styless.tabcontainer]}>
//             <View style={styles.absoluteCenter}>
//                 <Text style={[styles.headerText]}>{title}</Text>
//             </View>
//             <View>
//             </View>
//         </View>
//     </SafeAreaView>
// );

const TabButton = (props) => {
    const navigation = useNavigation()
    console.log(navigation)
    return <></>
}

const UserHomeStack = () => {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="Home"
                component={HomeScreen}
                options={{headerShown: false}}
                />
        </Stack.Navigator>
    );
};


// Title of the drawer header for the focused tab. Used from the drawer screen's `options`
// (React Navigation 7 does not re-run the parent's layout effect when only the nested tab changes).
export function getHeaderTitle(route) {
    const routeName = getFocusedRouteNameFromRoute(route) ?? '探索';

    switch (routeName) {
        case '探索':
            return '探索';
        case '推薦':
            return '推薦';
        case '行程':
            return '行程';
        case '個人':
            return '個人';
        case '社群':
            return '社群';
    }
}

const Tabs = ({navigation, route}) => {

    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                headerShown:false,
            // header: () => <CustomHeader title={route.name} />,
                tabBarLabelStyle: {
                    fontSize: 18,
                    fontWeight: 'bold',
                },
                tabBarActiveTintColor: "#7ed957",
            })}
        >
            <Tab.Screen name="探索"  component={UserHomeStack} options={{
                tabBarIcon: ({ focused }) => (
                    <View>
                        <Iconm name="explore" size={22}/> 
                    </View>
                ),
            }}/>
            <Tab.Screen name="推薦" component={RecommendationsTab} options={{
                tabBarIcon: ({ focused }) => (
                    <View>
                        <Iconf name="search" size={22}/>
                    </View>
                ),
            }}/>
            <Tab.Screen name="行程" component={ItineraryTab}
                options={{
                    tabBarIcon: ({ focused }) => (
                        <View>
                            <Icona name="calendar" size={22}/>
                        </View>
                    ),
                }}

            />
            <Tab.Screen name="個人" component={ProfileStackScreen} options={{
                // hidden tab (opened from the drawer); display:none so it does not take up space in the tab bar
                tabBarButton:() => null,
                tabBarItemStyle: { display: 'none' },
                tabBarIcon: ({ focused }) => (
                    <View>
                        <Icona name="calendar" size={22}/>
                    </View>
                ),
            }}/>

        </Tab.Navigator>
    );
}

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


export default Tabs;