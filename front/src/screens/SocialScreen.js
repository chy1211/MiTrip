import React, { useState, useEffect, useRef, useCallback } from 'react';
import { PLACEHOLDER_PHOTO } from '../constants';
import { SafeAreaView, ScrollView, View, Text, TouchableOpacity, Image, StyleSheet, Dimensions, Linking, ActivityIndicator } from 'react-native';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { useNavigation, useRoute } from '@react-navigation/native';
import Animated, { Extrapolation, interpolate, useAnimatedStyle, useSharedValue, withSpring } from "react-native-reanimated";
import { Ionicons as IconI, FontAwesome as IconF, AntDesign as Icona, MaterialCommunityIcons as IconM, FontAwesome5 as IconF5, Entypo as IconE  } from '@expo/vector-icons';
import { GestureHandlerRootView, Gesture, GestureDetector, FlatList } from 'react-native-gesture-handler';
import DraggableFlatList, { ScaleDecorator } from "react-native-draggable-flatlist";
import MapView, { Marker } from 'react-native-maps';
import { TripRouteLines, regionForTrips, formatTravelTime } from '../components/tripRoute';
import DateTimePicker from '@react-native-community/datetimepicker'
import Modal from 'react-native-modal';
import DateTimePickerModal from 'react-native-modal-datetime-picker';
import { API_BASE_URL } from '../constants/config';


const { height: SCREEN_HEIGHT } = Dimensions.get("window");
const MAX_TRANSLATE_Y = -SCREEN_HEIGHT;
const BOTTOM_SHEET_HEIGHT = hp(70);
const DRAG_LIST = hp(35); 
export default function SocialScreen(props) {
    const item = props.route.params;
    // const { params } = route.params;
    const navigation = useNavigation();
    const [tripDetail, setTripDetail] = useState([]);
    const [tripTimeResults, setTripTimeResults] = useState([]);
    const [tripArray, setTripArray] = useState();
    const [isLoading, setIsLoading] = useState(true);
    const [isDragEnd, setIsDragEnd] = useState(false);

    useEffect(() => {

        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/schedule/select_by_id/${item.scheduleID}`);
                const data = await response.json();
                
            // 更新组件状态，显示获取到的详细信息
                setTripDetail(data);
            } catch (error) {
                console.error('Error fetching restaurant details:', error);
            }
        };
        
        
        fetchData();
        
    }, []);
    useEffect(() => {

        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/schedule/select_by_id/${item.scheduleID}`);
                const data = await response.json();
                
            // 更新组件状态，显示获取到的详细信息
                setTripDetail(data);
            } catch (error) {
                console.error('Error fetching restaurant details:', error);
            }
        };
        
        
        fetchData();
        
    }, [isDragEnd]);
    const tripTime = tripDetail.filter((item) => item.tripType != 'Days');
    
    // useEffect(() => {
    //     async function getDistanceAndTimeResults() {
    //         const distanceAndTimeResults = await fetchDistanceAndTimeSequentially(tripTime);
            
    //         setTripTimeResults(distanceAndTimeResults.flat());
    //     };
    //     setIsLoading(false);
    //     getDistanceAndTimeResults();
        
    // }, [isDragEnd]);
    // useEffect(() => {
    //     const tripArray = [...tripDetail, ...tripTimeResults];
    //     setTripArray(tripArray);
    // }, [tripTimeResults]);
    
    
    
    // 以下為BS相關code
    const translateY = useSharedValue(0);

    const TPosition = -SCREEN_HEIGHT * 93.2 / 100;

    
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
        // console.log(event.translationY);
        translateY.value = event.translationY + context.value.y;
        translateY.value = Math.max(translateY.value, -730);
        translateY.value = Math.min(translateY.value, -710);
    })
    .onEnd(() => {
        if (translateY.value <  -SCREEN_HEIGHT/1.3) {
            scrollto(TPosition);
    }   else if (translateY.value > -SCREEN_HEIGHT/1.3 && translateY.value < -SCREEN_HEIGHT/2.5){
            scrollto(MAX_TRANSLATE_Y/1.5)
    }
    })

    useEffect(() => {
        translateY.value = withSpring(-SCREEN_HEIGHT / 1.5, {damping: 50});
    }, []);

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
        return {
            borderRadius,
            height,
            transform: [{ translateY: translateY.value }],
        };
    });

    // 以上為BS相關code
    const updateCategoriesData = Object.keys(tripDetail).map((category) => {
        if (tripDetail[category].photos === null) {
            return tripDetail[category].photos = PLACEHOLDER_PHOTO;
        }else {
            return tripDetail[category].photos;
        }

    });


    


    const DraggableListCard = ({ item, index, drag, isActive, tripTimeResult }) => {
        const [modalVisible, setModalVisible] = useState(false);
        const [selectedDate, setSelectedDate] = useState(new Date());
        const [date, setDate] = useState(new Date())
        const nextTrip = tripDetail[tripDetail.indexOf(item) + 1];
        console.log("index:",nextTrip);
        function extractHourAndMinute(dateTimeString) {
            const dateObject = new Date(dateTimeString);
            const hours = dateObject.getHours();
            const minutes = dateObject.getMinutes();
            
            // 處理顯示格式，例如補零
            const formattedHours = hours < 10 ? `0${hours}` : `${hours}`;
            const formattedMinutes = minutes < 10 ? `0${minutes}` : `${minutes}`;
            
            return `${formattedHours}:${formattedMinutes}`;
        }
        const handlePress = () => {
            setModalVisible(true);
        };
    
        const handleCancel = () => {
            setModalVisible(false);
        };
    
        const onChange = (event, selectedDate) => {
            const currentDate = selectedDate || date;
            setDate(currentDate);
            console.log('Selected date:', selectedDate);
            // 在這裡處理選擇的日期
        };

        const handleConfirm = () => {
            // 在這裡處理確定按鈕的邏輯，並將選擇的時間傳遞給後端
            const formattedDate = selectedDate.toISOString(); // 格式化日期
            // 調用後端 API，發送時間數據
    
            // 關閉 Modal
            setModalVisible(false);
        };
        const deleteTripData = async (item) => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/trips/${item.tripID}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },                
            });
                setIsDragEnd(true);
                const data = await response.json();
            } catch (error) {
                console.error('Error fetching restaurant details:', error);
            }
        };

        // 當 tripTimeResult 發生變化時，更新組件狀態
        console.log('tripTimeResult:', tripTimeResults);
        const tripTypeData = tripDetail.filter((item) => item.tripType != 'Days');
        const startDate = new Date(item.tripStartDate);
        const durationHours = new Date(item.durationHours);
        // console.log('tripTimeResult:', tripTimeResults);
        return (
            <View style={[ 
                
                // { borderColor: isActive ? "#E0E0E0" : '#000' },
                // { borderWidth: isActive ? 2 : 0 }
            ]} >
                <ScaleDecorator  >
                    
                    <View style={[ 
                        styles.listcontainer,
                    ]} >
                        <TouchableOpacity 
                            style={{ alignItems:'center', justifyContent:'center', height:hp(10), width:wp(10) }}
                            onPress={() => setModalVisible(true)}
                        >
                                <Text style={{ color:'#fff', fontSize:14, alignSelf:'center', fontWeight:'bold' }} >{extractHourAndMinute(item.tripStartDate)}</Text>
                                <IconI name='location-sharp' size={65} style={{ color:'#7ed957'}}/>
                                <Text style={{ color:'#fff', fontSize:14, alignSelf:'center', fontWeight:'bold' }} >{extractHourAndMinute(item.tripEndDate)}</Text>
                                <View style={{ position:'absolute', backgroundColor:'#fff', borderRadius:20, height:wp(2.2), width:wp(2.2), justifyContent:'center', alignItems:'center', right:22, bottom:30, borderColor:'#7ed957', borderWidth:1.5  }} >
                                    <Text style={{ color:'#000', fontSize:14, alignSelf:'center' }} >{tripTypeData.indexOf(item)+1}</Text>
                                </View>
                                <View style={{ backgroundColor:'#fff', position:'absolute', left: wp(3.68), top: wp(4.4), borderWidth:1.5, borderRadius:20, borderColor:'#7ed957', width: 21,height:21
                                }} >
                                    <IconE name='edit' size={15} style={{ color:'#000', alignSelf:'center'  }}/>
                                </View>
                        </TouchableOpacity>
                        <Modal visible={modalVisible} animationType='slide'
                            
                            transparent={true}
                            style={{ width: wp(100), height: hp(100) }}
                        >
                            <View style={{ flex: 1,
                                    justifyContent: 'center',
                                    alignItems: 'center',
                                    alignSelf:'center',
                                    padding: 20,
                                    width:600,
                                    height:400,
                                    backgroundColor:'#000',
                                    padding: 20,
                                    marginVertical:300,
                                    borderRadius:25,
                                }} >
                                <DateTimePicker
                                    mode='date'
                                    display='spinner'
                                    value={startDate}
                                    style={{ color:'#000' }}
                                    onChange={onChange}
                                    
                                />
                                <DateTimePicker
                                    mode='time'
                                    display='spinner'
                                    value={durationHours}
                                    style={{ color:'#000' }}
                                    locale="es-ES"
                                    onChange={onChange}
                                />
                                <View style={{ flexDirection:'row', marginTop:30 }} >
                                    <TouchableOpacity onPress={() => handleConfirm}>
                                        <Text style={{ color:'#fff', fontSize:30 }} >確定</Text>
                                    </TouchableOpacity>

                                    <TouchableOpacity onPress={() => setModalVisible(false)}>
                                        <Text style={{ color:'#fff', fontSize:30, marginLeft:100 }} >取消</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </Modal>
                        <TouchableOpacity
                        activeOpacity={1}
                        onLongPress={drag}
                        disabled={isActive}
                        style={[
                            styles.rowItem,
                        ]}
                        >
                            <Image source={{ uri: item.photos }} style={{ width:wp(10), height:wp(10), borderRadius: 8, marginLeft:10, alignSelf:'center' }} />
                            <Text style={styles.text}>{item.tripName}</Text>
                        </TouchableOpacity>
                    </View>
                    <View style={{ flexDirection:'row', left:hp(8.4) }} >
                        {nextTrip && nextTrip.tripType != "Days" && formatTravelTime(item.toNextTripHours, item.toNextTripMinutes) && (
                        <>
                        <IconF5 name='car' size={30} style={{ color:'#fff' }}/>

                        <Text style={{ color:'#fff', fontSize:20, alignSelf:'center', marginLeft:10 }} >{formatTravelTime(item.toNextTripHours, item.toNextTripMinutes)}</Text>
                        </>
                        )}
                    </View>
                    
                </ScaleDecorator>
            </View>
        );
    };

    
    const renderItem = ({ item, index, drag, isActive }) => {
        if (item.tripType == 'Days' && item.tripName != '第1天') {
            return (
                <View style={{ backgroundColor:'#fff', height:hp(5), justifyContent:'center' }} >
                    <Text style={{ color:'#000', fontSize:20, alignSelf:'center' }} >{item.tripName}</Text>
                </View>
            );
        }else if ( item.tripID != null ){
            const tripTimeResult = tripTimeResults[index];
            
            return (
                <DraggableListCard item={item} index={index} isActive={isActive} tripTimeResult={tripTimeResult} />
            );
        }
    };

    

// 以下為行車時間相關code
    
    
    
// 以上為行車時間相關code
    




    if (!tripDetail || tripDetail.length === 0) {
        return <ActivityIndicator size="large" color={"#000"} style={{ top:200 }} />;
    }

    return (
            <GestureHandlerRootView style={{flex: 1}}>
                <SafeAreaView style={{flex:1}}>
                    <View style={{backgroundColor:'white', height:hp(5)}}>
                        <TouchableOpacity 
                        onPress={() => navigation.goBack()}
                        style={{  width:wp(8), height:hp(5), justifyContent:'center',alignContent:'center' }}
                        >
                            <IconI name='chevron-back-outline' size={30} style={{alignSelf:'center'}}/>  
                        </TouchableOpacity>
                    </View>
                    <MapView style={{height:hp(27.5), justifyContent: 'center'}}
                        // ref={mapViewRef}
                        initialRegion={regionForTrips(tripTime)}
                        >
                        <TripRouteLines trips={tripTime} />
                        {Object.keys(tripTime).map (place =>(
                            <Marker key={place} coordinate={{ latitude: tripTime[place].lat, longitude: tripTime[place].lng }} title={tripTime[place].tripName} >
                                <View style={{ alignSelf:'center' }} >
                                    <IconF name='map-marker' size={40} color={'#E43A3A'}/>
                                </View>
                            </Marker>
                        ))}
                    </MapView>
                    <GestureDetector gesture={gesture}>
                        <Animated.View style={[styles.bottomsheetContainer, rBottomsSheetStyle]} > 
                            <View style={{}}>
                                <View style={styles.line} />
                            </View>                                                                                    
                            <View styles={{ width: wp(100), height:50 }} >
                                <Text style={{ fontSize:30, color:'#fff', marginLeft:20, marginVertical:15 }}  >{item.name}</Text>
                            </View>                                                               
                            <DraggableFlatList
                                data={tripDetail}
                                ListHeaderComponent={() => (

                                    <View style={{ backgroundColor:'#fff', height:hp(5), justifyContent:'center' }} >
                                        <Text style={{ color:'#000', fontSize:20, alignSelf:'center' }} >{tripDetail[0].tripName}</Text>
                                    </View>

                                    
                                )}
                                renderItem={renderItem}
                                keyExtractor={(item, index) => index.toString()}
                                style={{ height: hp(57) }}
                                
                                
                            />
                                
                        </Animated.View>
                    </GestureDetector>
                </SafeAreaView> 
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
        height: BOTTOM_SHEET_HEIGHT,
        width: wp(100),
        backgroundColor: "#000",
        position: "absolute",
        top: SCREEN_HEIGHT,
        borderRadius: 20,
        flex:1,
        paddingBottom:20,
    },
    line: {
        width: 75,
        height: 5, 
        backgroundColor: "grey",
        alignSelf: "center",
        marginVertical: 15,
        borderRadius: 5
    },
    cutline: {
        width: wp(100),
        height: 2,
        backgroundColor: '#fff',
        alignSelf: "center",
        marginBottom: 15,
    },
    comtext: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#fff',
        marginLeft: 15,
    },
    rowItem: {
        height: wp(12),
        width: wp(80),
        alignItems: "center",
        flexDirection: "row",
    },
    text: {
        color: "#fff",
        fontSize: 24,
        fontWeight: "bold",
        textAlign: "center",
        marginLeft: 20,
    },
    listcontainer: {
        flexDirection:'row',
        alignItems:'center',
        justifyContent:'center',
        height: hp(12),
        backgroundColor: '#000',
        width: wp(100),
    },
    draglist: {
        height: DRAG_LIST,
    },

});




