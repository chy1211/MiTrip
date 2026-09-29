import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import HomeScreen from './HomeScreen';
import RecommendationsScreen from './RecommendationsScreen';
import ItineraryScreen from './ItineraryScreen'; 
import SocialScreen from './SocialScreen';

const Tab = createBottomTabNavigator();

const TabNavigator = () => {
    return (
        <NavigationContainer sceneContainerStyle={{paddingVertical: 20}} >
            <Tab.Navigator  >
                <Tab.Screen name="Home" component={HomeScreen} />
                <Tab.Screen name="Recommendations" component={RecommendationsScreen} />
                <Tab.Screen name="Itinerary" component={ItineraryScreen} />
                <Tab.Screen name="Social" component={SocialScreen} />
            </Tab.Navigator>
        </NavigationContainer>
    );
};

export default TabNavigator;
