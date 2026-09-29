import { View, Text, TouchableOpacity, Image, ScrollView, ActivityIndicator } from 'react-native';
import React, { useState, useEffect } from 'react';
import { styles } from '../screens/styles';
import { theme } from '../theme';
import { categoriesData } from '../constants';
import { FlatList } from 'react-native-gesture-handler';
import { useNavigation } from '@react-navigation/native';
import { useCityData } from '../Context/CityDataContext';
import { API_BASE_URL } from '../constants/config';


export default function Categories2() {

    const [cityData, setCityData] = useState();
    const navigation = useNavigation();
    useEffect(() => {

        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/explore/checkHottestCity`);
                const json = await response.json();
                setCityData(json);

            } catch (error) {
                console.error(error);

            }
        };
        fetchData();

        
    }, []);

    const handleNavigation = (data) => {
        navigation.navigate('推薦', { data });
    };

    if (!cityData || cityData.length === 0) {
        return <ActivityIndicator size="large" color={"#fff"} />;
    }

    return (
        <View style={{marginTop: 30}}>
            <View style={{flexDirection: 'row', alignContent: 'center', justifyContent: 'space-between'}}>
                <Text style={{fontSize: 20, fontWeight: 'bold',color: 'white' }}>熱門城市</Text>
            </View>
            <ScrollView horizontal={true} contentContainerStyle={{paddingHorizontal: 1, marginTop: 10}}  showsHorizontalScrollIndicator={false}>
                {Object.keys(cityData.data).map(city => (
                    <View key={city} style={{ marginRight: 15, alignItems: 'center' }}>  
                        <TouchableOpacity 
                            onPress={() => {
                                if (handleNavigation) {
                                    handleNavigation(cityData.data[city]);
                                } else {
                                    console.error("handleNavigation is undefined");
                                }
                            }}
                            style={{alignItems: 'center'}}
                        >
                            <Image source={{ uri: cityData.data[city].photo }} style={{width: 150, height: 150, borderRadius: 8}} />
                            <Text style={{color: 'white', fontSize: 20}}>{cityData.data[city].labels}</Text>
                        </TouchableOpacity>
                    </View>
                    ))}
            </ScrollView>
        </View>
    );
}
