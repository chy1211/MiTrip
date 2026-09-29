import React, { useState, useEffect, useRef, useCallback,useContext } from 'react';
import { SafeAreaView, ScrollView, View, Text, TouchableOpacity, Image, StyleSheet, Dimensions, Linking, ActivityIndicator } from 'react-native';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { useNavigation, useRoute } from '@react-navigation/native';
import Animated, { Extrapolation, interpolate, useAnimatedStyle, useSharedValue, withSpring } from "react-native-reanimated";
import { Ionicons as Iconi, FontAwesome as IconF, AntDesign as Icona, MaterialCommunityIcons as IconM  } from '@expo/vector-icons';
import MapView, { Marker } from 'react-native-maps';
import { categoriesData, PLACEHOLDER_PHOTO } from '../constants';
import { GestureHandlerRootView, Gesture, GestureDetector, FlatList } from 'react-native-gesture-handler';
import {  Button } from 'react-native-paper';
import MyContext from '../components/context';
import CommentPlace from './CommentPlace';
import { AuthContext } from '../Context/AuthContext';
import { API_BASE_URL } from '../constants/config';
import { addToSchedule, tripTypeOf } from '../components/addToSchedule';

const { height: SCREEN_HEIGHT } = Dimensions.get("window");

const MAX_TRANSLATE_Y = -SCREEN_HEIGHT;
const BOTTOM_SHEET_HEIGHT = hp(69.5);

export default function DetailScreen(props) {
    const item = props.route.params;
    const dataType = item.dataType;

    console.log(item);

    const navigation = useNavigation();
    const mapViewRef = useRef(null);
    const [restaurantDetails, setRestaurantDetails] = useState([]);
    const [restaurantComment, setRestaurantComment] = useState([]);
    const {userID} = useContext(AuthContext);
    const [onPressHandle, setOnPressHandle] = useState(false);
    console.log(restaurantDetails);
    const openGoogleMaps = () => {
        const url = `https://www.google.com/maps/dir/?api=1&destination=${restaurantDetails[0].lat},${restaurantDetails[0].lng}`
        Linking.openURL(url)
    };
    // console.log(restaurantDetails);
    const searchPlaceOnGoogle = () => {
        // 使用店名构建 Google 搜索链接
        const url = `https://www.google.com/search?q=${item.name}`;
    
        // 打开链接
        Linking.openURL(url)
        .catch((err) => console.error('無法打開連結', err));
    };

    const fetchRestaurantComment = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/${dataType}/${item.id}/reviews`);
            const data = await response.json();

        // 更新组件状态，显示获取到的详细信息
            setRestaurantComment(data);
        
        } catch (error) {
            console.error('Error fetching restaurant comments:', error);
        }
    };
    useEffect(() => {
        fetchRestaurantComment();
    }, [onPressHandle]);

    useEffect(() => {

        const fetchRestaurantDetails = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/${dataType}/${item.id}?user_id=${userID}`);
                const data = await response.json();

            // 更新组件状态，显示获取到的详细信息
                setRestaurantDetails(data);
            } catch (error) {
                console.error('Error fetching restaurant details:', error);
            }
        };
        
        fetchRestaurantDetails();
        fetchRestaurantComment();

    }, []);
    console.log(restaurantDetails,"restaurantDetails");
    console.log(restaurantComment,"restaurantComment");

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

        translateY.value = event.translationY + context.value.y;
        translateY.value = Math.max(translateY.value, TPosition);
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
    const openweb = () => {
        const url = restaurantDetails[0].website;
        Linking.openURL(url)
    }; 

    const facebookweb = "https://www.facebook.com/";
    
    const reviewsWithNewlines = restaurantComment[3];
    let processedData = [];
    if(restaurantComment && restaurantComment.length > 0) {
        processedData = restaurantComment.map(item => {
            // 對每個元素的第三個項目進行替換
            const replacedString = item[3].replace(/\\\\n/g, '\n');
            
            // 返回替換後的元素
            return [...item.slice(0, 3), replacedString, ...item.slice(4)];
        });
    }

    const updateCategoriesData = Object.keys(restaurantDetails).map((category) => {
        if (restaurantDetails[category].photos === null) {
            return restaurantDetails[category].photos = PLACEHOLDER_PHOTO;
        }else {
            return restaurantDetails[category].photos;
        }

    });
    const OnPressChange =(data) =>{
        setOnPressHandle(!data);
    }


    const renderItem = ({ item }) => (
        <View style={{  }} >
            <View style={styles.cutline} />
            <View style={{ flexDirection:'row',marginBottom:20 }} >
                <View style={{ width:wp(10.5), marginLeft:14.5 }} >
                    <IconM name="account-circle-outline" size={40} color={'#fff'} style={{ alignSelf:'center' }} />
                    <Text style={{ color:'#fff', alignSelf: 'center' }}  >
                        {item[1] === 0 ? 'GoogleMaps使用者評論' : `${item[1]}`}
                    </Text>
                </View>
                <View style={{ width:wp(8), justifyContent:'center' }} >
                    <View style={{ flexDirection: 'row', width: wp(8), justifyContent: 'center' }}>
                        <IconF name="star" size={22} color={'#ff0'} style={{ alignSelf: 'center' }} />
                        <Text style={{ color: 'white', fontSize: 22, marginLeft: 5, fontWeight: 'bold', alignSelf: 'center', flexWrap: 'nowrap' }}>
                            {item[1] === 0 ? '-.-' : `${item[4]}`}
                        </Text>
                    </View>
                </View>
                <View style={{ width:wp(75), justifyContent:'center' }} >
                    {item[2] !== null && item[2] !== undefined && ( 
                        <Text style={styles.comtext} >{typeof item[2] === 'string' ? new Date(item[2]).toLocaleDateString() : item[2]}</Text>
                    )}
                    <Text style={styles.comtext} >{item[3]}</Text>
                    
                </View>
            </View>
            
        </View>
    );
    if (!restaurantDetails || restaurantDetails.length === 0 ) {
        return <ActivityIndicator size="large" color={"#fff"} />;
    }

    return (
            <GestureHandlerRootView style={{flex: 1}}>
                    <SafeAreaView style={{flex:1}}>
                        <View style={{backgroundColor:'white', height:hp(5)}}>
                            <TouchableOpacity 
                            onPress={() => navigation.goBack()}
                            style={{  width:wp(8), height:hp(5), justifyContent:'center',alignContent:'center' }}
                            >
                                <Iconi name='chevron-back-outline' size={30} style={{alignSelf:'center'}}/>  
                            </TouchableOpacity>
                        </View>
                        <MapView style={{height:hp(27.5), justifyContent: 'center'}}
                            // ref={mapViewRef}
                            initialRegion={{ latitude: restaurantDetails[0].lat, longitude: restaurantDetails[0].lng, latitudeDelta: 0.01, longitudeDelta: 0.01 }}
                            >
                            <Marker coordinate={{ latitude: restaurantDetails[0].lat, longitude: restaurantDetails[0].lng }} title={restaurantDetails[0].name} >
                                <View style={{ alignSelf:'center' }} >
                                    <IconF name='map-marker' size={40} color={'#E43A3A'}/>
                                </View>
                                <Text>{restaurantDetails[0].formatted_address}</Text>
                            </Marker>
                        </MapView>
                        <GestureDetector gesture={gesture}>
                            <Animated.View style={[styles.bottomsheetContainer, rBottomsSheetStyle]} >
                                <View style={{}}>
                                    <View style={styles.line} />
                                </View>                                                                                        
                                    
                                <FlatList
                                    data={processedData}
                                    keyExtractor={(item) => item[0]}
                                    ListHeaderComponent = {() => (
                                        <View key={restaurantDetails[0].id} style={{flex:1, marginBottom: 20, paddingHorizontal: 14.5, paddingBottom:5, backgroundColor:'#000', width: wp(100)}}>
                                            <View style={{  }} >
                                                <View style={{ flexDirection:'row', marginBottom:10 }} >
                                                    <Image source={{ uri: restaurantDetails[0].photos }} style={{ width:hp(25), height:hp(25), borderRadius:8 }} />
                                                    <View>
                                                        <View style={{ flexDirection:'row', width:wp(50), marginLeft:20 }} >
                                                            <Text style={{ width:wp(30), fontSize: 20, fontWeight: 'bold', color:'#fff' }}>{restaurantDetails[0].name}</Text>
                                                            <IconF name="star" size={22} color={'#ff0'} style={{ alignSelf:'center' }} />                                                            
                                                            <Text style={{color: 'white', fontSize:22, marginLeft:5, fontWeight: 'bold'}}>{restaurantDetails[0].rating}</Text>
                                                            <Text style={{color: 'white', fontSize:15, alignSelf:'center'}}>({restaurantDetails[0].user_ratings_total})</Text>
                                                        </View>
                                                        <View>
                                                            {restaurantDetails[0].class ? (
                                                            <Text style={{ fontSize: 16, fontWeight: 'bold', color:'#fff', marginLeft:20, marginTop: 5 }}>餐廳分類: {restaurantDetails[0].class}</Text>
                                                            ) : (
                                                            <Text style={{ fontSize: 16, fontWeight: 'bold', color:'#fff', marginLeft:20, marginTop: 5 }}>餐廳分類: 暫無分類</Text>
                                                            )}                                                            
                                                        </View>
                                                        <View style={{ flexDirection:'row', marginLeft:20, height:hp(20) }} >
                                                            <TouchableOpacity 
                                                                onPress={() => openGoogleMaps()}
                                                                style={{ flexDirection:'row', backgroundColor:'#fff', width:wp(10), height:45, justifyContent:'center', borderRightWidth:1, borderRightColor:'gray', alignSelf:'flex-end'  }} 
                                                            >
                                                                <View style={{ flexDirection:'row', alignItems:'center', width:56 }} >
                                                                    <IconM name="navigation-outline" size={25} color={'#000'} style={{  }} />
                                                                    <Text style={{  }} >導航</Text>
                                                                </View>
                                                            </TouchableOpacity>
                                                            <TouchableOpacity 
                                                                onPress={() => searchPlaceOnGoogle()}
                                                                style={{ flexDirection:'row', backgroundColor:'#fff', width:wp(13), height:45, justifyContent:'center', borderRightWidth:1, borderRightColor:'gray', alignSelf:'flex-end'}} 
                                                            >
                                                                <View style={{ flexDirection:'row', alignItems:'center' }} >
                                                                    <Icona name="google" size={25} color={'#000'} style={{  }} />
                                                                    <Text style={{ marginLeft:8 }} >Google!</Text>
                                                                </View>
                                                            </TouchableOpacity>
                                                            {restaurantDetails[0].website !== null && restaurantDetails[13] !== undefined && (
                                                            <React.Fragment>
                                                                {restaurantDetails[0].website.includes(facebookweb) ? (
                                                                // 当 restaurantDetails[13] 包含 facebookweb 时显示的内容
                                                                <TouchableOpacity 
                                                                    onPress={() => openweb()}
                                                                    style={{ flexDirection:'row', backgroundColor:'#fff', width:wp(15), height:45, justifyContent:'center', borderRightWidth:1, borderRightColor:'gray', alignSelf:'flex-end'}} 
                                                                >
                                                                    <View style={{ flexDirection:'row', alignItems:'center' }} >
                                                                        <IconM name="facebook" size={30} color={'#000'} style={{  }} />
                                                                        <Text style={{ marginLeft:8 }} >Facebook!</Text>
                                                                    </View>
                                                                </TouchableOpacity>
                                                                ) : (
                                                                // 当 restaurantDetails[13] 不包含 facebookweb 时显示的内容
                                                                <TouchableOpacity 
                                                                    onPress={() => openweb()}
                                                                    style={{ flexDirection:'row', backgroundColor:'#fff', width:wp(15), height:45, justifyContent:'center', borderRightWidth:1, borderRightColor:'gray', alignSelf:'flex-end'}}
                                                                >
                                                                    <View style={{ flexDirection:'row', alignItems:'center' }} >
                                                                        <IconM name="web" size={25} color={'#000'} style={{  }} />
                                                                        <Text style={{ marginLeft:8 }} >官方網站</Text>
                                                                    </View>
                                                                </TouchableOpacity>
                                                                )}
                                                            </React.Fragment>
                                                            )}                                                            
                                                        </View>
                                                    </View>
                                                    <TouchableOpacity style={{ justifyContent:'center' }}
                                                        onPress={() => addToSchedule({ userID, tripType: tripTypeOf(dataType), tripId: item.id })}
                                                    >
                                                        <View style={{  }} >
                                                            <Icona name="plus-circle" size={50} color={'white'}  />
                                                        </View>
                                                    </TouchableOpacity>
                                                </View>
                                                <View style={{ flexDirection:'row', alignContent:'center', marginBottom:15,  }} >
                                                    <IconF name='map-marker' size={30} style={{ color:'#fff', width:30.5, textAlign:'center' }}/>
                                                    <Text style={{ fontSize: 16, fontWeight: 'bold', color:'#fff', marginLeft:15, alignSelf:'center' }}>
                                                        {restaurantDetails[0].formatted_address}
                                                    </Text>
                                                </View>
                                                <View style={{ flexDirection:'row' }} >
                                                    <Iconi name='time-outline' size={30} style={{ color:'#fff' }}/>
                                                    {restaurantDetails[0].opening_hours ? (
                                                    <Text style={{ fontSize: 16, fontWeight: 'bold', color: '#fff', marginLeft: 15, marginTop: 6 }}>
                                                    {restaurantDetails[0].opening_hours.map((item, index) => (
                                                        <React.Fragment key={index}>
                                                        {item}
                                                        {'\n'}
                                                        </React.Fragment>
                                                    ))}
                                                    </Text>
                                                ) : (
                                                    <Text style={{ fontSize: 16, fontWeight: 'bold', color: '#fff', marginLeft: 15, marginTop: 6 }}>
                                                    店家並未提供營業時間
                                                    </Text>
                                                )}
                                                </View>
                                                
                                            </View>
                                        </View>
                                    )}
                                    renderItem={renderItem}
                                    ListFooterComponent={() => (
                                        <CommentPlace
                                            restaurantName={restaurantDetails[0].name}
                                            restaurantId={restaurantDetails[0].id}
                                            dataType={dataType}
                                            OnPressChange ={OnPressChange}
                                            onCommentSubmit={() => {
                                                fetchRestaurantComment();
                                            }}
                                        />
                                    )}
                                    style={{ width: wp(100), marginBottom: 13 }}    
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
        flex: 1,
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


});