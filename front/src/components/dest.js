import { View, Text, TouchableOpacity, Image, ScrollView, ActivityIndicator, Linking } from 'react-native'
import React, { useState, useEffect } from 'react'
import { destinationData } from '../constants'
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { LinearGradient } from 'expo-linear-gradient'
import { HeartIcon } from 'react-native-heroicons/solid';
import { useNavigation } from '@react-navigation/native';
import { API_BASE_URL } from '../constants/config';

export default function Destinations2() {
    const navigation = useNavigation();
    const [hottestData, setHottestData] = useState([]);
    

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/explore/get_news`,{
                    method: 'GET',
                });
                const json = await response.json();
                setHottestData(json);
            } catch (error) {
                console.error(error);
            }
        };
        fetchData();
        
    }, []);

    if (!hottestData || hottestData.length === 0) {
        return <ActivityIndicator size="large" color={"#fff"} />;
    }
    return (
        <View style={{ flex: 1}}  >
            <ScrollView  horizontal contentContainerStyle={{ flexDirection: 'row', justifyContent: 'space-between', paddingVertical: hp(2) }} contentOffset={{ x: 0, y: 0 }}>
                {hottestData.data.map((item, index) => (
                    <TouchableOpacity 
                        key={ index }
                        onPress={() => Linking.openURL(item.src)}
                        style={{ alignItems: 'center', marginRight: wp(4) }}
                    >
                        <Image source={{uri : item.photo}} style={{ width: 300, height: 200, borderRadius: 8 }} />
                        <Text style={{ color: 'white', marginTop: 5, fontSize:20 }}  >{item.title}</Text>
                    </TouchableOpacity>
                ))}
            </ScrollView>
        </View>
    )
}

// const DestinationCard = ({ item, navigation }) => {
//     const [isFavourite, toggleFavourite] = useState(false);

//     return (
//         <TouchableOpacity style={{ alignItems: 'center', marginRight: wp(4) }}>
//             <Image source={hottestData.photo} style={{ width: 300, height: 200, borderRadius: 8 }} />
//             <Text style={{ color: 'white', marginTop: 5 }}>{hottestData.labels}</Text>
//         </TouchableOpacity>
//     )
// }
