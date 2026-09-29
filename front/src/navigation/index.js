import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/HomeScreen';
import SocialScreen from '../screens/SocialScreen';
import RecommendationsScreen from '../screens/RecommendationsScreen';
import ProfileScreen from '../screens/ProfileScreen';
import Tabs from './tabs';
import ItineraryScreen from '../screens/ItineraryScreen';
import MyDrawers from './drawer';
import { StatusBar } from "expo-status-bar";
import DetailScreen from '../screens/DetailScreen';
import EditItineraryScreen from '../screens/editItineraryScreen';
import Categories2 from '../components/categories2';
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import ForgetPasswordScreen from '../screens/ForgetPasswordScreen';
import UpdatePasswordScreen from '../screens/UpdatePasswordScreen';
import Questionnaire from '../screens/Questionnaire';
import QuestionnairefetchData from '../components/QuestionnaireFetch';

const Stack = createNativeStackNavigator();


function AppNavigator() {
    return (
            <Stack.Navigator initialRouteName='Drawer' screenOptions={{headerShown: false}}>
                <Stack.Screen name='Home' component={HomeScreen} />
                <Stack.Screen name='Recommendations' component={RecommendationsScreen} />
                <Stack.Screen name='Itinerary' component={ItineraryScreen} />
                <Stack.Screen name='Social' component={SocialScreen} />
                <Stack.Screen name='Profile' component={ProfileScreen} />
                <Stack.Screen name='Tabs' component={Tabs} />
                <Stack.Screen name='Drawer' component={MyDrawers} />
                <Stack.Screen name='Detail' component={DetailScreen} />
                <Stack.Screen name='Edit' component={EditItineraryScreen} />
                <Stack.Screen name='Cate' component={Categories2} />
                <Stack.Screen name="Login" component={LoginScreen}/>
                <Stack.Screen name="Register" component={RegisterScreen}/>
                <Stack.Screen name="ForgetPassword" component={ForgetPasswordScreen}/>
                <Stack.Screen name="UpdatePassword" component={UpdatePasswordScreen}/>
                <Stack.Screen name="Questionnaire" component={Questionnaire}/>
                <Stack.Screen name="QuestionnairefetchData" component={QuestionnairefetchData}/>
            </Stack.Navigator>

    );
}

export default AppNavigator;