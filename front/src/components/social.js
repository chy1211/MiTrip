import { View, Text, TouchableOpacity, Image, ScrollView, FlatList } from 'react-native'
import React, { useState, useEffect, useContext } from 'react'
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { useNavigation } from '@react-navigation/native';
import { num } from '../constants';
import {AntDesign as Icona} from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { AuthContext } from '../Context/AuthContext';
import { API_BASE_URL } from '../constants/config';

const storeData = async (key, value) => {
    try {
        await AsyncStorage.setItem(key, value)
    } catch (error) {
        console.log("storeData error", error)
    }
};

const getData = async (key) => {
    try {
        const value = await AsyncStorage.getItem(key)
        if (value !== null) {
            return value
        }
    } catch (error) {
        console.log("getData error", error)
    }
};


export default function Social() {
    const navigation = useNavigation();
    const [destinationData, setDestinationData] = useState([])
    const {userID} = useContext(AuthContext);
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/explore/checkHottestSchedule?user_id=${userID}`,{
                    method: 'GET',
                });
                const json = await response.json();
                setDestinationData(Object.values(json.data));
            } catch (error) {
                console.error(error);
            }
        };
        fetchData();
        
    }, []);

    return (
        <View style={{marginTop: 30}} key={destinationData.id}>
            <View>
                <Text style={{fontSize: 20, fontWeight: 'bold', color: 'white' }}>熱門行程</Text>
            </View>
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', flexWrap: 'wrap' }}>
                {
                    destinationData.map((item) => (
                        <SocialCard
                            item={item}
                            key={item.scheduleID}
                            navigation={navigation}
                            setDestinationData={setDestinationData}
                        />
                    ))
                }
            </View>
        </View>
    );
}


const SocialCard = ({ item, navigation, setDestinationData }) => {
    const [isFavourite, toggleFavourite] = useState(item.liked);
    const [count, setCount] = useState(item.numberofLikes);
    const {userID} = useContext(AuthContext);

    useEffect(() => {
        getData(item.scheduleID.toString()).then(storedValue => {
            if (storedValue !== null) {
                setCount(parseInt(item.numberofLikes));
                toggleFavourite(item.liked);
            }
        });
    }, []);


    const handleFavouritePress = () => {
        const scheduleId = item.scheduleID.toString();
        
        fetch(`${API_BASE_URL}/api/explore/likeSchedule?user_id=${userID}&schedule_id=${scheduleId}`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            const updatedLiked = !item.liked;
    
            // 立即更新 isFavourite 狀態
            toggleFavourite(updatedLiked);
    
            // 根據按讚狀態更新 count
            setCount(prevCount => (updatedLiked ? prevCount + 1 : prevCount - 1));

            // 更新 item
            const updatedItem = {...item, liked: updatedLiked, numberofLikes: count}; 
            setDestinationData(prev => 
            prev.map(i => i.scheduleID === item.scheduleID ? updatedItem : i)
            );
            // 更新 AsyncStorage
            storeData(scheduleId, updatedLiked ? "true" : "false");
        })
        .catch(error => {
            console.error('API 請求錯誤:', error);
        });
    };
    
    return (
        <View style={{flexDirection:'row'}} key={item.scheduleID}>
            <TouchableOpacity onPress={()=> navigation.navigate('Social', {...item})} style={{ marginTop:10, flexDirection:'column', position: 'relative', borderRadius: 8, overflow: 'hidden' }}>
                {/* 2x2 photo grid. A plain View instead of FlatList: at most 4 photos, and a vertical
                    FlatList inside HomeScreen's ScrollView triggers the nested-VirtualizedList error. */}
                <View style={{ width: wp(44), flexDirection: 'row', flexWrap: 'wrap' }}>
                    {item.photos.filter(photo => photo !== null).slice(0, 4).map((photo, index) => (
                        <Image
                            key={index.toString()}  // 使用 index 作為 key
                            source={{ uri: photo }}
                            style={{
                                width: wp(44) / 2,
                                height: hp(45) * 0.5,
                                borderRadius: 8,
                                overflow: 'hidden'
                            }}
                        />
                    ))}
                </View>
                <LinearGradient 
                    colors={['transparent', 'rgba(0,0,0,0.8)']}
                    style={{ position: 'absolute', width: wp(44), height: hp(15), borderRadius: 8, top: hp(45) - hp(15) }}
                    start={{ x: 0.5, y: 0 }}
                    end={{ x: 0.5, y: 0.7 }}
                
                />

                <Text style={{ color: 'white', position:'absolute', top:hp(36), fontSize:20, marginLeft:15 }}>{item.name}</Text>
                <Text style={{ color: 'white', position:'absolute', top:hp(39), fontSize:15, marginLeft:15 }}>{item.Describe}</Text>
                <View style={{flexDirection:'row', marginTop:hp(1), marginBottom:hp(3), marginLeft:wp(1)}}>
                    <TouchableOpacity onPress={handleFavouritePress} style={{flexDirection:'row'}}>
                        {isFavourite ? (
                        <Icona name='heart' size={20} color={'red'}/>
                        ) : (
                        <Icona name='heart' size={20} color={'white'}/>
                        )}
                        <Text style={{ color: 'white', marginLeft:wp(1), fontWeight:'bold' }}>{count}個讚</Text>
                    </TouchableOpacity>
                    <Text style={{ color: 'white', marginLeft:wp(23) }}>{item.timeStamp}</Text>

                </View>
            </TouchableOpacity>

        </View>
    )
}
