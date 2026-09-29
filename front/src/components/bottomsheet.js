import { StyleSheet, Text, View, Dimensions, TouchableOpacity, Image, Modal } from "react-native";
import React, { useEffect, useCallback, useState, useContext} from "react";
import { Gesture, GestureDetector, ScrollView, TextInput } from "react-native-gesture-handler";
import Animated, { Extrapolation, interpolate, useAnimatedStyle, useSharedValue, withSpring, withTiming } from "react-native-reanimated";
import Icon from '@expo/vector-icons/FontAwesome';
import { widthPercentageToDP as wp, heightPercentageToDP as hp, heightPercentageToDP } from 'react-native-responsive-screen';
import Icona from '@expo/vector-icons/AntDesign';
import CheckBox from 'expo-checkbox';
import { useNavigation } from '@react-navigation/native';
import { categoriesData, PLACEHOLDER_PHOTO } from "../constants";
import { AuthContext } from "../Context/AuthContext";
import { API_BASE_URL } from '../constants/config';


const { height: SCREEN_HEIGHT } = Dimensions.get("window");

const MAX_TRANSLATE_Y = -SCREEN_HEIGHT;

const PAGE_SIZE = 5;


const BottomSheet = () => {
    const translateY = useSharedValue(0);
    const [isLoading, setIsLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const navigation = useNavigation();
    const {userID} = useContext(AuthContext);

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
            scrollto(MAX_TRANSLATE_Y/6)
    }   else if (translateY.value < -SCREEN_HEIGHT/1.3) {
            scrollto(MAX_TRANSLATE_Y);
    }   else if (translateY.value > -SCREEN_HEIGHT/1.3 && translateY.value < -SCREEN_HEIGHT/2.5){
            scrollto(MAX_TRANSLATE_Y/1.5)
    }
    })

    useEffect(() => {
        translateY.value = withSpring(-SCREEN_HEIGHT / 1.5, {damping: 50});
    }, []);

    const [categoriesData, setCategoriesData] = useState([]);


    

    useEffect(() => {
        const fetchData = async () => {
        try {
            setIsLoading(true);
            const response = await fetch(`${API_BASE_URL}/api/restaurant?user_id=${userID}&lat=22.774424&lng=120.399112`);
            const json = await response.json();
            setCategoriesData(json);
            setIsLoading(false);
        } catch (error) {
            console.error(error);
            setIsLoading(false);
        }
    };
        fetchData();
    }, []);

    const updateCategoriesData = categoriesData.map((category) => {
        if (category[7] === null) {
            return category[7] = PLACEHOLDER_PHOTO;
        }else {
            return category[7];
        }

    });


    

    const rBottomsSheetStyle = useAnimatedStyle(() => {
        const borderRadius = interpolate(
            translateY.value, 
            [MAX_TRANSLATE_Y + 200,MAX_TRANSLATE_Y], 
            [30,0],
            Extrapolation.CLAMP
        );
        return {
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
    const [searchText, setSearchText] = useState('');

    return (
        

        <GestureDetector gesture={gesture} style={{  }}>
            <Animated.View style={[styles.bottomsheetContainer, rBottomsSheetStyle]} >
                <View style={{ height:hp(5) }}>
                    <View style={styles.line} />
                </View>
                <ScrollView  horizontal style={{ height:hp(5) }}>
                    <View style={{flexDirection:'row'}}>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button1' && styles.selectedButton]}
                            onPress={() => handlePress('button1')}
                        >
                            <Text style={styles.buttonText}>餐廳</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button2' && styles.selectedButton]}
                            onPress={() => handlePress('button2')}
                        >
                            <Text style={styles.buttonText}>景點</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button3' && styles.selectedButton]}
                            onPress={() => handlePress('button3')}
                        >
                            <Text style={styles.buttonText}>住宿</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[styles.button, selectedButton === 'button4' && styles.selectedButton]}
                            onPress={() => setModalVisible(true)}
                        >
                            <Text style={styles.buttonText}>更多..</Text>
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
                                            value={selectedFilters.option1}
                                            onValueChange={() => handleFilterSelection('option1')}
                                        />
                                        <Text>選項1</Text>
                                    </View>
                                    <View style={styles.checkboxContainer}>
                                        <CheckBox
                                            value={selectedFilters.option2}
                                            onValueChange={() => handleFilterSelection('option2')}
                                        />
                                        <Text>選項2</Text>
                                    </View>
                                    <View style={styles.checkboxContainer}>
                                        <CheckBox
                                            value={selectedFilters.option3}
                                            onValueChange={() => handleFilterSelection('option3')}
                                        />
                                        <Text>選項3</Text>
                                    </View>
                                    <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeButton}>
                                        <Text style={styles.closeButtonText}>關閉</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </Modal>
                    </View>
                </ScrollView>
                
                <View style={{ marginVertical:10 }}>
                    <View id="filters">
                        <TextInput
                            style={{width:wp(90), height:hp(3.5), backgroundColor:'white', borderRadius:5, alignSelf:'center', justifyContent:'flex-start'}}
                            placeholder="搜尋餐廳"
                            onChangeText={(text) => setSearchText(text)}
                        />
                    </View>
                </View>

                <ScrollView  contentContainerStyle={{ flexDirection: 'column', justifyContent: 'space-between', marginTop:15 }}
                    onScroll={({ nativeEvent }) => {
                        const { layoutMeasurement, contentOffset, contentSize } = nativeEvent;
                        const paddingToBottom = 20;
                        // if (layoutMeasurement.height + contentOffset.y >= contentSize.height - paddingToBottom) {
                        //     fetchData();
                        // }
                    }}
                    // scrollEventThrottle={5}
                >
                    {
                        categoriesData.map((category, index) => {
                            return (
                                                                    
                                <View key={index} style={{flex:1, flexDirection:'row', marginBottom: 20, marginHorizontal:wp(2.5)}}>
                                
                                    <TouchableOpacity onPress={(event) => {
                                        navigation.navigate('Detail', {...category});
                                        
                                    }}
                                        style={{flexDirection:'row', flex:5}}>
                                        
                                        <Image source={{ uri: category[7] }} style={{width: wp(20), height: hp(15), borderRadius: 8,flex:1}} />
                                        <View style={{ marginLeft: 20, alignItems: 'flex-start', flexDirection: 'column',flex:3}}>
                                            <View style={styles.titlecon}>
                                                <Text style={{color: 'white', fontSize:25}}>{category[1]}</Text>
                                            </View>
                                            <View style={styles.starcon}>
                                                <View style={{flexDirection:'row'}}>
                                                    <Icon name="star" size={22} color={'#ff0'} style={{alignSelf:'center'}} />
                                                    <Text style={{color: 'white', fontSize:22}}>{category[3]}</Text>
                                                </View>

                                            </View>
                                            <View style={styles.container}>
                                                <Text style={category[2] === "休息中" ? styles.redText : (category[2] === null ? styles.yellowText : styles.whiteText)}>
                                                    {category[2] || "未提供營業時間資訊"}
                                                </Text>
                                            </View>                                  
                                        </View>
                                    </TouchableOpacity>
                                    <TouchableOpacity style={{ flexDirection:'row', alignItems:'center',justifyContent:'flex-end', flex:1 }}>
                                        <Icona name="plus-circle" size={50} color={'white'}/>
                                    </TouchableOpacity>
                                </View>
                            );
                        })
                    }
                </ScrollView>
            </Animated.View>
        </GestureDetector>
    );
};



const styles = StyleSheet.create({
    bottomsheetContainer: {
        height: hp(89),
        width: wp(100),
        backgroundColor: "black",
        position: "absolute",
        top: SCREEN_HEIGHT,
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
        color:'white',
    },
    selectedButton: {
        borderBottomWidth: 4,
        borderBottomColor: 'white', // 底部的顏色
        
    },
    buttonText: {
        fontSize: 18,
        color:'white',
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
        padding: 35,
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: {
        width: 0,
        height: 2,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
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
        alignSelf: 'flex-end',
    },
    closeButtonText: {
        fontSize: 16,
        color: 'blue',
    },
    checkboxContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
    },
});

export default BottomSheet;