import React, { useEffect, useCallback, useState, useContext } from 'react';
import { PLACEHOLDER_PHOTO } from '../constants';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, Image, Modal, Dimensions, Alert } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { Ionicons as Iconi, FontAwesome as IconF, AntDesign as Icona, MaterialIcons as IconM } from '@expo/vector-icons';
import { Gesture, GestureDetector, TextInput, GestureHandlerRootView, FlatList } from "react-native-gesture-handler";
import Animated, { Extrapolation, interpolate, useAnimatedStyle, useSharedValue, withSpring, withTiming } from "react-native-reanimated";
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import CheckBox from 'expo-checkbox';
import { useNavigation } from '@react-navigation/native';
import { BottomSheet } from '@rneui/base';
import { AuthContext } from '../Context/AuthContext';
import { API_BASE_URL } from '../constants/config';

const { height: SCREEN_HEIGHT } = Dimensions.get("window");

const MAX_TRANSLATE_Y = -SCREEN_HEIGHT;

const BOTTOM_SHEET_HEIGHT = hp(69.5);

// React 19 ignores defaultProps on function components, so defaults are merged here.
const DEFAULT_PROPS = {
    "labels": "高雄市",
    "lat": 22.6167954,
    "lng": 120.3110824,
};

const RecommendationsScreen = (screenProps) => {
    const props = { ...DEFAULT_PROPS, ...screenProps };
    const routeData = props.route.params;
    const [cityData, setCityData] = useState();
    const [categoriesData, setCategoriesData] = useState([]);
    const translateY = useSharedValue(0);
    const [isLoading, setIsLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const navigation = useNavigation();
    const [lastRestaurantId, setLastRestaurantId] = useState(null);
    const [searchText, setSearchText] = useState('');
    const [mapLocation, setMapLocation] = useState({lat: 22.774424, lng: 120.399112 });
    const [userSchedule, setUserSchedule] = useState([]);
    const [dataType, setDataType] = useState('restaurant');
    const [dataType2, setDataType2] = useState('Restaurant');
    const [isRateFour, setIsRateFour] = useState(false);
    const [isOpening, setIsOpening] = useState(false);
    const {userID} = useContext(AuthContext);
    const [isReSet, setIsReSet] = useState(false);
    // const [textInputValue, setTextInputValue] = useState('');
    // console.log(mapLocation);
    const TPosition = -SCREEN_HEIGHT * 93.2 / 100;
    
    

    const handleNavigation = (cityData) => {
        setMapLocation(cityData);
        fetchDataA(cityData);
    };

    const scrollto = useCallback((destination, number) => {
        'worklet';
        translateY.value = withSpring(destination, { damping: 50 })
    }, [])

    const context = useSharedValue({ y: 0 });
    const gesture = Gesture.Pan()
    .onStart(() => {
        context.value = { y: translateY.value}
    })
    .onUpdate((event) => {
        translateY.value = event.translationY + context.value.y;
        translateY.value = Math.max(translateY.value, MAX_TRANSLATE_Y);
    })
    .onEnd(() => {
        if (translateY.value > -SCREEN_HEIGHT/2.5){
            scrollto(MAX_TRANSLATE_Y/7)
    }   else if (translateY.value < -SCREEN_HEIGHT/1.3) {
            scrollto(MAX_TRANSLATE_Y);
    }   else if (translateY.value > -SCREEN_HEIGHT/1.3 && translateY.value < -SCREEN_HEIGHT/2.5){
            scrollto(MAX_TRANSLATE_Y/1.5)
    }
    })

    useEffect(() => {
        translateY.value = withSpring(-SCREEN_HEIGHT / 1.5, {damping: 50});
    }, []);

    
    useEffect(() => {
        if (routeData !== undefined) {
            setMapLocation(Object.values(routeData)[0]);
        }
    }, [props]);


    useEffect(() => {
        const fetchDataAndUpdateMap = async () => {
            await fetchDataA(mapLocation);
        };
    
        fetchDataAndUpdateMap();
        const updatedRegion = {
            latitude: mapLocation.lat || 22.774424,
            longitude: mapLocation.lng || 120.399112,
            latitudeDelta: mapLocation.latitudeDelta || 0.04,
            longitudeDelta: mapLocation.longitudeDelta || 0.04,
        };
        setRegion(updatedRegion);
    }, [mapLocation]);

    const [region, setRegion] = useState({
        latitude: mapLocation.lat,
        longitude: mapLocation.lng,
        latitudeDelta: mapLocation.latDelta,
        longitudeDelta: mapLocation.lngDelta,
    });
    
    useEffect(() => {
        // 當 mapLocation 變化時，更新地圖區域
        setRegion({
            latitude: mapLocation.lat,
            longitude: mapLocation.lng,
            latitudeDelta: mapLocation.latitudeDelta,
            longitudeDelta: mapLocation.longitudeDelta,
        });
    }, [mapLocation]);

    useEffect(() => {
        fetchDataA(mapLocation);
    }, [dataType]);

    useEffect(() => {
        fetchDataA(mapLocation);
    }, []);

    useEffect(() => {
        fetchDataA(mapLocation);
        setIsOpening(false);
        setIsRateFour(false);
    }, [isReSet]);

    useEffect(() => {
        setCategoriesData(Object.values(categoriesData).filter(item => parseFloat(item.rating) >= 4 ))
    },[isRateFour===true]);

    useEffect(() => {
        setCategoriesData(Object.values(categoriesData).filter(item => item.ifOpening === '營業中'))
    },[isOpening===true]);

    

    const fetchDataA = async (location) => {
        try {
            setIsLoading(true);
            const response = await fetch(`${API_BASE_URL}/api/${dataType}?user_id=${userID}&lat=${location.lat}&lng=${location.lng}`);
            const json = await response.json();
            // console.log(json);
            setCategoriesData(json);
            setIsLoading(false);
        } catch (error) {
            console.error(error);
            setIsLoading(false);
        }
    };

    const fetchData = async () => {
        if (searchText !== '') {
            try {
                setIsLoading(true);
                const response = await fetch(`${API_BASE_URL}/api/${dataType}/search?keyWord=${searchText}&lat=22.774424&lng=120.399112`);
                const json = await response.json();
                setCategoriesData(json);
                setIsLoading(false);
            } catch (error) {
                console.error(error);
                setIsLoading(false);
            }
        }
    };

    const fetchAttractionData = async () => {
        try {
            setIsLoading(true);
            const response = await fetch(`${API_BASE_URL}/api/restaurant?user_id=${userID}&lat=${location.lat}&lng=${location.lng}`);
            const json = await response.json();
            // console.log(json);
            setCategoriesData(json);
            setIsLoading(false);
        } catch (error) {
            console.error(error);

        }
    };
    useEffect(() => {
        const fetchUserSchedule = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/schedule/select_by_user_id/${userID}`)
                const json = await response.json();
                setUserSchedule(json);
            } catch (error) {
                console.error(error);
            }
        };
        fetchUserSchedule();
    }, []);


    const updateCategoriesData = Object.keys(categoriesData).map((category) => {
        if (categoriesData[category].photos === null) {
            return categoriesData[category].photos = PLACEHOLDER_PHOTO;
        }else {
            return categoriesData[category].photos;
        }

    });


    const rBottomsSheetStyle = useAnimatedStyle(() => {
        const borderRadius = interpolate(
            translateY.value, 
            [MAX_TRANSLATE_Y + 200,TPosition], 
            [20,0],
            Extrapolation.CLAMP
        );
        const height = interpolate(
            translateY.value, 
            [MAX_TRANSLATE_Y + 350,TPosition], 
            [BOTTOM_SHEET_HEIGHT, BOTTOM_SHEET_HEIGHT + 280],
            Extrapolation.CLAMP
        );
        const paddingBottom = interpolate(
            translateY.value, 
            [MAX_TRANSLATE_Y + 350,TPosition], 
            [150, 60],
            Extrapolation.CLAMP
        );
        return {
            paddingBottom,
            height,
            borderRadius,
            transform: [{ translateY: translateY.value }],
        };
    });
    const [selectedButton, setSelectedButton] = useState('button1');

    const handlePress = (buttonName) => {
        setSelectedButton(buttonName);
    };


    const [modalVisible, setModalVisible] = useState(false);
    const [selectedFilters, setSelectedFilters] = useState({
        option1: false,
        option2: false,
        option3: false,
    });

    const handleFilterSelection = (key) => {
        setSelectedFilters(prevState => ({
        ...prevState,
        [key]: !prevState[key],
        }));
    };

    const postData = async (scheduleID,item) => {
        console.log('ID:',scheduleID);
        const data1 = {
            "scheduleID": scheduleID,
            "trip_type": dataType2,
            "trip_id": item.id,
            "user_id": userID,
        };

        const response = await fetch(`${API_BASE_URL}/api/trips`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data1)
        });
    
        if (!response.ok) {
            throw new Error('HTTP error ' + response.status);
        }
    
        return response.json();
    }

    const handlePressAdd = (userSchedule,item) => {
        const options = Object.keys(userSchedule).map(schedule => ({
            
            text: userSchedule[schedule].name, 
            onPress: () => handleScheduleSelection(userSchedule[schedule].scheduleID,item)
            
        }));
    
        options.push({ text: "取消", onPress: () => console.log("取消"), style: "cancel" });
        
        console.log(item);
        Alert.alert(
            "新增到行程",
            "請選擇要新增到哪一個行程",
            options,
            { cancelable: true }
        );
    };
    const handleScheduleSelection = async (scheduleID,item) => {
        
        
        try {
            const result = await postData(scheduleID,item);
            Alert.alert("成功", "已成功新增到行程");
        } catch (error) {
            console.error(error);
        }
    };
    
    
    
    const renderItem = ({ item }) => (
            <View style={{ flex: 1, flexDirection: 'row', marginBottom: 20, marginHorizontal: wp(2.5) }} key={item.id}>
                <TouchableOpacity
                    onPress={(event) => {
                    setLastRestaurantId(item);
                    navigation.navigate('Detail', { ...item, dataType });
                }}
                style={{ flexDirection: 'row', flex: 5 }}
                >
                    <Image source={{ uri: item.photos }} style={{ width: wp(20), height: hp(15), borderRadius: 8, flex: 1 }} />
                    <View style={{ marginLeft: 20, alignItems: 'flex-start', flexDirection: 'column', flex: 3 }}>
                        <View style={styles.titlecon}>
                            <Text style={{ color: 'white', fontSize: 25 }}>{item.name}</Text>
                        </View>
                        <View>
                            {item.class ? (
                            <Text style={{ fontSize: 16, fontWeight: 'bold', color:'#fff', marginBottom:20 }}>分類: {item.class}</Text>
                            ) : (
                            <Text style={{ fontSize: 16, fontWeight: 'bold', color:'#fff', marginBottom:20 }}>分類: 暫無分類</Text>
                            )}                                                            
                        </View>
                        <View style={styles.starcon}>
                            <View style={{ flexDirection: 'row' }}>
                                <IconF name="star" size={22} color={'#ff0'} style={{ alignSelf: 'center' }} />
                                {item.rating ? (
                                <Text style={{ color: 'white', fontSize: 22 }}>{item.rating}</Text>
                                ) : (
                                <Text style={{ color: 'white', fontSize: 22 }}>暫無評分</Text>
                                )}                                
                            </View>
                        </View>
                        {dataType !== 'hotel' && (
                            <View style={styles.container}>
                                <Text style={item.ifOpening === '休息中' ? styles.redText : item.ifOpening === null ? styles.yellowText : styles.whiteText}>
                                    {item.ifOpening || '未提供營業時間資訊'}
                                </Text>
                            </View>
                        )}
                    </View>
                </TouchableOpacity>
                <TouchableOpacity style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-end', flex: 1 }}
                    onPress={() => handlePressAdd(userSchedule,item) }
                >
                    <Icona name="plus-circle" size={50} color={'white'} />
                </TouchableOpacity>
            </View>
        
    );

    return (
        <GestureHandlerRootView style={{flex: 1}}>
            <MapView
                style={styles.map}
                region={
                    region.latitudeDelta && region.longitudeDelta
                        ? region
                        : {
                                latitude: region.latitude,
                                longitude: region.longitude,
                                latitudeDelta: 0.04,
                                longitudeDelta: 0.04,
                        }
                }
                onRegionChangeComplete={(newRegion) => {
                    const newMapLocation = {
                        lat: newRegion.latitude,
                        lng: newRegion.longitude,
                        latitudeDelta: newRegion.latitudeDelta,
                        longitudeDelta: newRegion.longitudeDelta,
                    };
                    handleNavigation(newMapLocation);
                }}
            >
                {Object.keys(categoriesData).map(place => (
                    <Marker
                    key={place}
                    coordinate={{
                        latitude: categoriesData[place].lat,
                        longitude: categoriesData[place].lng,
                    }}
                    title={categoriesData[place].name}
                    
                >
                        <View>
                            <TouchableOpacity 
                            onPress={() => {
                                const selectedPlace = categoriesData[place];
                                navigation.navigate('Detail', { ...selectedPlace, dataType });
                            }} >
                                <IconF name='map-marker' size={40} color={'#E43A3A'}/>
                            </TouchableOpacity>
                        </View>
                        
                    </Marker>
                ))}
            </MapView>
            <GestureDetector gesture={gesture} style={{  }}>
                <Animated.View style={[styles.bottomsheetContainer, rBottomsSheetStyle]} >
                    <View style={{  }}>
                        <View style={styles.line} />
                    </View>
                    <View style={{ flexDirection:'row'  }}>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button1' && styles.selectedButton]}
                            onPress={() => {handlePress('button1'),setDataType('restaurant'),setDataType2('Restaurant');}}
                        >
                            <Text style={[styles.buttonText, selectedButton === 'button1' && styles.selectedText]}>餐廳</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button2' && styles.selectedButton]}
                            onPress={() => {handlePress('button2'); setDataType('attraction'),setDataType2('Attraction');}}
                        >
                            <Text style={[styles.buttonText, selectedButton === 'button2' && styles.selectedText]}>景點</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button3' && styles.selectedButton]}
                            onPress={() => {handlePress('button3'); setDataType('hotel'),setDataType2('Hotel'); }}
                        >
                            <Text style={[styles.buttonText, selectedButton === 'button3' && styles.selectedText]}>住宿</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button4' && styles.selectedButton]}
                            onPress={() => setModalVisible(true)}
                        >
                            <Text style={[styles.buttonText, selectedButton === 'button4' && styles.selectedText]}>更多..</Text>
                        </TouchableOpacity>
                        <Modal
                            animationType='fade'
                            transparent={true}
                            visible={modalVisible}
                            onRequestClose={() => {
                            setModalVisible(false);
                            }}
                            style={{borderRadius:1}}
                        >
                            <View style={styles.centeredView}>
                                <View style={styles.modalView}>
                                    <View style={styles.checkboxContainer}>
                                        <CheckBox
                                            value={isRateFour}
                                            onValueChange={() => setIsRateFour(!isRateFour)}
                                        />
                                        <Text style={{ fontSize:22 }} >店家評分大於等於4</Text>
                                    </View>
                                    {dataType !== 'hotel' && (
                                    <View style={styles.checkboxContainer}>
                                        <CheckBox
                                            value={isOpening}
                                            onValueChange={() => setIsOpening(!isOpening)}
                                        />
                                        <Text style={{ fontSize:22 }} >只顯示營業中的店家</Text>
                                    </View>
                                    )}
                                    <View style={{ flexDirection:'row', alignSelf:'center', marginTop:30 }} >
                                        <TouchableOpacity onPress={() => setIsReSet(!isReSet)} style={styles.closeButton}>
                                            <Text style={styles.closeButtonText}>重置</Text>
                                        </TouchableOpacity>
                                        <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeButton}>
                                            <Text style={styles.closeButtonText}>關閉</Text>
                                        </TouchableOpacity>
                                    </View>
                                </View>
                            </View>
                        </Modal>
                    </View>
                    
                    <View style={{ marginVertical:10 }}>
                        {dataType === 'restaurant' && (
                            <View id="filters">
                                <TextInput
                                    style={{width:wp(90), height:hp(3.5), backgroundColor:'white', borderRadius:5, alignSelf:'center', justifyContent:'flex-start'}}
                                    placeholder="     搜尋餐廳..."
                                    onChangeText={(text) => setSearchText(text)}
                                    returnKeyType='search'
                                    onSubmitEditing={fetchData}
                                />
                            </View>
                        )}
                        {dataType === 'attraction' && (
                            <View id="filters">
                                <TextInput
                                    style={{width:wp(90), height:hp(3.5), backgroundColor:'white', borderRadius:5, alignSelf:'center', justifyContent:'flex-start'}}
                                    placeholder="     搜尋景點..."
                                    onChangeText={(text) => setSearchText(text)}
                                    returnKeyType='search'
                                    onSubmitEditing={fetchData}
                                />
                            </View>
                        )}
                        {dataType === 'hotel' && (
                            <View id="filters">
                                <TextInput
                                    style={{width:wp(90), height:hp(3.5), backgroundColor:'white', borderRadius:5, alignSelf:'center', justifyContent:'flex-start'}}
                                    placeholder="     搜尋住宿..."
                                    
                                    onChangeText={(text) => setSearchText(text)}
                                    returnKeyType='search'
                                    onSubmitEditing={fetchData}
                                />
                            </View>
                        )}
                    </View>
                    <FlatList
                        data={Object.values(categoriesData)}
                        keyExtractor={(item) => item.id}
                        renderItem={renderItem}
                        
                    />
                    
                </Animated.View>
            </GestureDetector>
        </GestureHandlerRootView>
            
    );
}

const styles = StyleSheet.create({
    containerbox: {
        flex: 1,
        backgroundColor: 'white',
        justifyContent: 'center',
    },
    container: {
        flex: 1,
        justifyContent: 'center',
    },
    map: {
        flex: 1,
        width: '100%',
    },
    bottomsheetContainer: {
        height: hp(10),
        width: wp(100),
        backgroundColor: "black",
        position: "absolute",
        top: SCREEN_HEIGHT,
        flex:1,
        
    },
    line: {
        width: 75,
        height: 5, 
        backgroundColor: "grey",
        alignSelf: "center",
        marginVertical: 15,
        borderRadius: 5
    },
    container: {
        flexDirection:'row',
        alignContent:'center',
        justifyContent:'center',
    },
    titlecon: {
        flexDirection:'row',
        alignContent:'center',
        justifyContent:'center',
        flex:1,
    },
    starcon: {
        flexDirection:'row',

    },
    button: {
        paddingVertical:5,
        paddingHorizontal: 10,
        marginHorizontal: 10,
        color:'#7ed957',
    },
    selectedButton: {
        borderBottomWidth: 4,
        borderBottomColor: '#7ed957', // 底部的顏色
        
    },
    buttonText: {
        fontSize: 18,
        color:'#8E8E8E',
    },
    centeredView: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 22,
    },
    modalView: {
        margin: 20,
        backgroundColor: 'white',
        borderRadius: 20,
        padding: 45,
        alignItems: 'flex-start',
        shadowColor: '#000',
        shadowOffset: {
        width: 0,
        height: 2,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
    },
    whiteText: {
        color: 'white',
        fontSize: 22,
    },
    redText: {
        color: 'red',
        fontSize: 22,
    },
    yellowText: {
        color: 'yellow',
        fontSize: 22,
    },
    closeButton: {
        alignItems: 'center',
        justifyContent: 'center',
        marginHorizontal: 15,
    },
    closeButtonText: {
        fontSize: 22,
        color: '#7ed957',
    },
    checkboxContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
        justifyContent: 'center',
    },
    selectedText: {
        color: 'lightgray',
    },
});

export default RecommendationsScreen;