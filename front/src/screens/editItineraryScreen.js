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
import DateTimePicker from '@react-native-community/datetimepicker';
import Modal from 'react-native-modal';
import { API_BASE_URL } from '../constants/config';


const { height: SCREEN_HEIGHT } = Dimensions.get("window");
const MAX_TRANSLATE_Y = -SCREEN_HEIGHT;
const BOTTOM_SHEET_HEIGHT = hp(70);
const DRAG_LIST = hp(40); 
export default function EditItineraryScreen(props) {
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

    
    
    


    const DraggableListCard = ({ item, index, drag, isActive, tripTimeResult, departure }) => {

        const [modalVisible, setModalVisible] = useState(false);
        const [selectedDate, setSelectedDate] = useState(new Date());
        const [date, setDate] = useState(new Date());
        const [stayHour, setStayHour] = useState(0);
        const [stayMinute, setStayMinute] = useState(0);
        const [defaultDate, setDefaultDate] = useState(new Date());
        const currentIndex = tripDetail.indexOf(item);
        const[departureTime,setDepartureTime] = useState('');

        // const nextTrip = currentIndex < tripDetail.length - 1 ? tripDetail[currentIndex + 1] : tripDetail[currentIndex-1];
        const nextTrip = tripDetail[currentIndex + 1];
        console.log("nextTrip:",tripDetail[currentIndex]);
        // console.log("index:",item);
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
    
        const onChange = (data) => {
            const selectedDateTimestamp = data.nativeEvent.timestamp;
            const selectedDate = new Date(selectedDateTimestamp);
            console.log(selectedDate,'這是selectedDate');
            setDate(selectedDate);
            console.log(defaultDate,'這是defaultDate');
    
            const hours = selectedDate.getHours(); // 取得小時
            const minutes = selectedDate.getMinutes(); // 取得分鐘

            // const formattedDate = `${item.startdate}:${hours}:${minutes}`;
            console.log('this is item.startdate',item.tripStartDate);
            let tempDate = new Date(item.tripStartDate);

            const year = tempDate.getFullYear();
            const month = tempDate.getMonth() + 1; // 月份是從 0 開始的，所以要加 1
            const day = tempDate.getDate();

            const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:00`;

            // console.log('處理好的啟程時間',formattedDate);
            setDepartureTime(formattedDate);
            // console.log('處理好的啟程時間GOGOGOGO',departureTime);
        };
        
        const onStayTimeChange = (data) => {
        
            const selectedDateTimestamp = data.nativeEvent.timestamp;
            const selectedDate = new Date(selectedDateTimestamp);

            // const timezoneOffset = -8 * 60; // UTC+8 時區的偏移量（以分鐘為單位）
            // const localDate = new Date(selectedDate.getTime() + timezoneOffset * 60 * 1000);

            console.log(selectedDate,'這是selectedDate');
            setDefaultDate(selectedDate);
            console.log(defaultDate,'這是defaultDate');
    
    
            const hours = parseInt(selectedDate.getHours()); // 取得小時
            const minutes = parseInt(selectedDate.getMinutes()); // 取得分鐘

    
            setStayHour(hours);
            setStayMinute(minutes);
            // console.log('小時:',hours);
            // console.log('StayHour小時',stayHour);
            
        }

        const handleConfirm = async () => {
            // 在這裡處理確定按鈕的邏輯，並將選擇的時間傳遞給後端
            // const formattedDate = selectedDate.toISOString(); // 格式化日期
            // console.log(stayHour,'這是StayHour');
            // console.log(stayMinute,'這是StayMinute');
            // console.log(departureTime,'這是departureTime');
            // 調用後端 API，發送時間數據
            const data1 = {
                "new_start_date": departureTime,
                "durationHour": stayHour,
                "durationMinute": stayMinute,
            }
    
    
            try {
                
                const response = await fetch(`${API_BASE_URL}/api/trips/${item.tripID}/update_time`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data1)
            });
                const data = await response.json();
                
            // 更新组件状态，显示获取到的详细信息
            } catch (error) {
                console.error('Error fetching restaurant details:', error);
            }
            setModalVisible(false);
        };
        const deleteTripData = async (item) => {
            try {
                setIsDragEnd(true);
                const response = await fetch(`${API_BASE_URL}/api/trips/${item.tripID}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },                
            });
                const data = await response.json();
            } catch (error) {
                console.error('Error fetching restaurant details:', error);
            }
            setIsDragEnd(false);
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
                            style={{  }}
                        >
                            <View style={{ 
                                    justifyContent: 'center',
                                    alignItems: 'center',
                                    alignSelf:'center',
                                    padding: 20,
                                    width:700,
                                    height:600,
                                    backgroundColor:'#000',
                                    padding: 20,
                                    marginVertical:300,
                                    borderRadius:25,
                                }} >
                                {/* <DateTimePicker
                                    mode='date'
                                    display='spinner'
                                    value={startDate}
                                    style={{ color:'#000' }}
                                    onChange={onChange}
                                    
                                /> */}
                                <View style={{flexDirection:'row',alignItems:'center'}}>
                                    <Text style={{color:'white',fontSize:20}}>啟程時間</Text>
                                    <DateTimePicker
                                        mode='time'
                                        display='spinner'
                                        value={date}
                                        style={{ color:'#000' }}
                                        locale="es-ES"
                                        is24Hour={true}
                                        onChange={(data) => onChange(data)}
                                    />
                                </View>
                                <View style={{flexDirection:'row',alignItems:'center'}}>
                                    <Text style={{color:'white',fontSize:20}}>停留時間</Text>
                                    <DateTimePicker
                                        mode='time'
                                        display='spinner'
                                        value={defaultDate}
                                        style={{ color:'#000' }}
                                        locale="es-ES"
                                        is24Hour={true}
                                        onChange={(data) => onStayTimeChange(data)}
                                    />
                                </View>
                                <View style={{ flexDirection:'row', marginTop:30 }} >
                                    <TouchableOpacity onPress={(item) => {handleConfirm(item);console.log(item)}}>
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
                        <TouchableOpacity style={{ width:wp(10), height:hp(10), alignItems:'center', justifyContent:'center' }}
                            onPress={() => deleteTripData(item)}
                        >
                            <IconM name='delete' size={30} style={{ color:'#fff' }}/>
                        </TouchableOpacity>
                    </View>
                    <View style={{ flexDirection:'row', left:hp(8.4) }} >
                        {(nextTrip && nextTrip.tripType != "Days" && formatTravelTime(item.toNextTripHours, item.toNextTripMinutes)) && (
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
                <DraggableListCard item={item} index={index} drag={drag} isActive={isActive} tripTimeResult={tripTimeResult} />
            );
        }
    };

    const ScheduleButtons = ({ schedule, onButtonPress }) => {
        const renderButtons = () => {
            const buttons = [];
    
            for (let day = 1; day <= schedule.days; day++) {
                const buttonLabel = `第 ${day} 天`;
                buttons.push(
                    <TouchableOpacity
                    key={day}
                    onPress={() => onButtonPress(day)}
                    style={{ 
                        backgroundColor:'#fff',
                        width:wp(15),
                        height:45,
                        justifyContent:'center',
                        borderRightWidth:2,
                        borderRightColor:'#D0D0D0',
                        alignSelf:'center'
                    }}
                    >
                    <Text style={{ color: '#000', alignSelf:'center', fontSize:20 }}>{buttonLabel}</Text>
                    </TouchableOpacity>
            );
            }
    
        return buttons;
        };
    
        return <View style={{ flexDirection:'row',width: wp(100), height:55, backgroundColor:'#D0D0D0', marginTop:20 }} >{renderButtons()}</View>;
    };

    // After a drag, send the new order (each stop tagged with the day header above it) to the backend,
    // which re-times the whole itinerary: first stop keeps the day's start time, every next stop
    // starts after the previous one ends plus the travel time. (The 2023 version only re-timed the
    // two neighbours of the dragged stop, so later stops overlapped or jumped to another day.)
    const onDragEnd = async ({ data }) => {
        setTripDetail(data);
        let day = 1;
        const order = [];
        data.forEach((trip) => {
            if (trip.tripType === 'Days') {
                day = trip.onDay;
            } else if (trip.tripID != null) {
                order.push({ tripID: trip.tripID, day });
            }
        });
        try {
            await fetch(`${API_BASE_URL}/api/schedule/${item.scheduleID}/reflow`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order }),
            });
        } catch (error) {
            console.error('Error re-timing the itinerary:', error);
        }
        setIsDragEnd((value) => !value); // refetch the new times
    };



    




    if (!tripDetail || tripDetail.length === 0) {
        return <ActivityIndicator size="large" color={"#000"} style={{ top:200 }} />;
    }else if (!tripTime || tripTime.length === 0) {
        return alert('請先新增行程');
    }
    

    return (
            <GestureHandlerRootView style={{flex: 1}}>
                <SafeAreaView style={{flex:1}}>
                    <View style={{backgroundColor:'white', height:hp(5), flexDirection:'row'}}>
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
                                <Text style={{ fontSize:22, color:'#fff', marginLeft:20 }}  >{item.name}</Text>
                                <Text style={{ fontSize:16, color:'#fff', marginLeft:20 }}  >{item.startDate}~{item.endDate}</Text>
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
                                style={{ height: hp(59) }}
                                onDragEnd={onDragEnd}
                                
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




