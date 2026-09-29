import  React, {useContext, useEffect, useState} from 'react';
import {View, StyleSheet, SafeAreaView, Alert,Image} from 'react-native';
import {Avatar,
        Title,
        Caption,
        Text,
        Button,
        Card,
        TouchableRipple, 
        Modal} from 'react-native-paper';

import { FontAwesome as IconF, MaterialCommunityIcons as Icon } from '@expo/vector-icons'
import { Gesture, GestureDetector, TextInput, GestureHandlerRootView, FlatList } from "react-native-gesture-handler";
import { useLinkProps } from '@react-navigation/native';
import EditProfileScreen from './EditProfileScreen';
import { useNavigation } from '@react-navigation/native';
import { AuthContext } from '../Context/AuthContext';
import { TouchableOpacity } from 'react-native-gesture-handler';
import { ActivityIndicator } from 'react-native-paper';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { AirbnbRating } from 'react-native-ratings';
import { API_BASE_URL } from '../constants/config';



export default function ProfileScreen() {
    const navigation = useNavigation();
    const {username} = useContext(AuthContext);
    const {userID} = useContext(AuthContext);
    const {userToken} = useContext(AuthContext);
    const [comment, setComment] = useState([]);
    const {email} = useContext(AuthContext);
    const {birthDay} = useContext(AuthContext);
    const [isDelete, setIsDelete] = useState(false);
    const [isVisible, setVisible] = useState(false);
    const [placeholder, setPlaceholder] = useState('');
    const [rateStars, setRateStars] = useState(0);
    const [reText, setReText] = useState('');
    const [dataType, setDataType] = useState('');
    const [textID, setTextID] = useState('');
    const [requestState, setRequestState] = useState('');

    // useEffect(() => {
    //     const userInfo = async() => {
    //         console.log({})
    //         const response = await fetchData(option='userInfo',
    //             username1='',
    //             password1='',
    //             checkPassword1='',
    //             email1='',
    //             birthDay1='',
    //             restaurantid='',
    //             userid='',
    //             text = '',
    //             userRating = '',
    //             Token=userToken
    //                 );
    //         console.log('GetEmail&Birthday',response);
    //         if (response.success) {
    //             // 在這裡你可以根據 responseData 做進一步的處理
    //             //設置email&Birth
                
    //             let email = JSON.stringify(response.data.info.email);
    //             let birthDay = JSON.stringify(response.data.info.birthDay);
    //             SetEmail(email);
    //             SetBirthday(birthDay);

    //         } else {
    //             // 如果有錯誤，顯示錯誤信息或者進行其他處理
    //             if (response.error) {
    //                 Alert.alert('Error', response.error);
    //                 return('error');
    //             } else {
    //                 // 如果錯誤信息不存在，顯示一般性錯誤提示
    //                 Alert.alert('Error', 'An error occurred during catching userinfo.');
    //             }
    //         }

    //     }
    //     userInfo();
    // }, []);
    const checkRecord = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/qes/isRecord/${userID}`);
            const data = await response.json();
            setRequestState(data.message);
            return data.message === 'isRecord.';
        } catch (err) {
            console.log(err);
            return false;
        }
    };
    const fetchUserComment = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/restaurant/userID/${userID}/reviews`)
            const json = await response.json();

            setComment(json);
        } catch (error) {
            console.error(error);
        }
    };
    useEffect(() => {
        
        fetchUserComment();
    }, []);

    useEffect(() => {
        fetchUserComment();
    }, [isDelete]);

    const handleDelete = async (item) => {
        Alert.alert(
            "刪除確認", // 警示訊息的標題
            "你確定要刪除這個項目嗎？", // 警示訊息的內容
            [
                {
                    text: "取消",
                    onPress: () => console.log("取消刪除"),
                    style: "cancel"
                },
                { 
                    text: "確定", 
                    onPress: async () => {
                        console.log('看一下',item.textID );
                        try {
                            const response = await fetch(`${API_BASE_URL}/api/${item.dataType}/deleteReview?textId=${item.textID}`,{
                                method: 'DELETE',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    textID: item.textID,
                                    dataType: item.dataType
                                })
                            })
                            const json = await response.json();
                            console.log(json);
                            setIsDelete(!isDelete);
                            return;
                        } catch (error) {
                            console.error(error);
                        }
                    }
                }
            ],
            { cancelable: false }
        );
    }

    const handleEdit = (item) => {
        setPlaceholder(item.text);
        setRateStars(item.userRating);
        setReText(item.text);
        setDataType(item.dataType);
        setTextID(item.textID);
        setVisible(!isVisible);
    }
    const handleCancel = () => {
        setVisible(!isVisible);
    }
    const handleConfirm = async () => {
        try {
            
            const response = await fetch(`${API_BASE_URL}/api/${dataType}/updateReview`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                textId: textID,
                newText: reText,
                newUserRating: rateStars
            
            })
        });
            const data = await response.json();
            setVisible(!isVisible);
            setIsDelete(!isDelete);
            return;
        } catch (error) {
            console.error('Error fetching restaurant details:', error);
            setVisible(!isVisible);
        }
        
    }


    const renderItem = ({item}) =>(
        <View style={{ justifyContent:'center', width:wp(100)}}>
            <View style={{ marginLeft:30, flexDirection:'row', flex:1 }} >
                <View style={{ justifyContent:'center', flex:1 }} >
                    <Image source={{ uri: item.photos }} style={{ width: wp(15), height: wp(15), borderRadius: 10, alignSelf:'center' }} />
                </View>
                <View style={{ marginLeft:20, flex:3 }} >
                    <Text style={{ color:'#fff', fontSize:20, marginTop:10 }} >
                        {item.name}
                    </Text>
                    <View style={{ flexDirection:'row', paddingTop:10 }} >
                        <IconF name="star" size={22} color={'#ff0'} style={{ alignSelf:'center' }} />
                        <Text style={{ color:'#fff', fontSize:20 }} >
                            {item.userRating}
                        </Text>
                        <Text style={{ color:'#fff', fontSize:20, marginLeft:20 }} >
                            {item.time}
                        </Text>
                    </View>
                    <View style={{ marginTop:20 }} >
                        <Text style={{ color:'#fff', fontSize:20 }} ellipsizeMode='tail'>
                            {item.text}
                        </Text>
                    </View>
                </View>
                <View style={{ marginLeft:20, justifyContent:'center', alignContent:'flex-end',flex:2, marginRight:20 }} >
                    <TouchableOpacity style={{ alignSelf:'flex-end' }}  onPress={() => {handleEdit(item), setVisible(!isVisible) }} >
                        <IconF name='edit' size={28} style={{ color:'#7ed957', paddingVertical:10, alignSelf:'flex-end' }}/>
                    </TouchableOpacity>
                    <TouchableOpacity style={{ alignItems:'center' }} onPress={() => handleDelete({textID: item.textID,dataType: item.dataType}) } >
                        <Icon name='delete' size={30} style={{ color:'red', alignSelf:'flex-end', paddingVertical:10 }}/>
                    </TouchableOpacity>
                </View>
                
            </View>
            <View style={styles.cutline} />
        </View>
        
    );
    

    if (!comment || comment.length === 0) {
        return <ActivityIndicator size="large" color={"#fff"} />;
    }


    return(
        <SafeAreaView style={styles.container}>

            <View style={styles.userInfoSection}>
                <View style={{flexDirection:'row',marginTop: 15}}>
                    
                
                    {username === null ? (
                        
                    <View style={{marginLeft:20,flexDirection:'row'}}>
                        <Avatar.Image
                        source={require('../../assets/images/avatar.png')}
                        size={120}/>
                        <Title style={[styles.title, {marginLeft:10, marginTop:45,color:'white' }]} >未登入</Title>
                        {/* <Caption style={styles.caption}>{username}</Caption> */}
                    </View>
                        ) : (
                        <View>
                            <View style={{marginLeft:20,flexDirection:'row'}}>
                                <Avatar.Image
                                source={require('../../assets/images/user_avatar.png')}
                                size={120}/>
                                <Title style={[styles.title, {marginLeft:10, marginTop:45,color:'white' }]} >{username}</Title>
                                
                            </View>
                            <TouchableOpacity style={{left:150,top:-10}} onPress={() => {
                                    navigation.navigate("UpdatePassword",{username1:username})
                                    console.log('Pressed')
                                    
                                }}>
                                <Text style={{fontWeight:'400',fontSize:16 ,color:'#7ed957'}}>
                                    更改密碼
                                </Text>
                            </TouchableOpacity>
                            {/* <Button mode="contained-tonal" style={{left:130,top:-30}}
                                onPress={() => {
                                    navigation.navigate("UpdatePassword",{username1:username})
                                    console.log('Pressed')
                                    
                                }}>
                                更改密碼
                            </Button> */}
                        </View>
                        )}        
                </View>
            </View>

            <View style={styles.userInfoSection}>
                <View style={styles.row}>
                    <Icon name='email' color='#fff' size={20} />
                    <Text style={{color:'#fff', marginLeft: 10 }}>
                        {email}
                    </Text>
                </View>
                <View style={styles.row}>
                    <Icon name='cake-variant' color='#fff' size={20} />
                    <Text style={{color:'#fff', marginLeft: 10 }}>
                        {birthDay}
                    </Text>
                </View>
                <View style={styles.row}>
                    <Icon name="clipboard-list" color='#fff' size={20}  style={{alignSelf:'center'}}/>
                    <Button mode="contained-tonal" style={{marginLeft: 10}}
                        onPress={async() => {
                            // wait for the check (2023 version read the previous, stale state and let users fill it in again)
                            if(await checkRecord()) {
                                Alert.alert('您已經填寫過');
                            } else {
                                navigation.navigate('Questionnaire'); 
                            }        
                        }}>
                        填寫行程偏好問卷
                    </Button>
                </View>
            </View>
            <View style={{ width:wp(100), height:hp(60) }}>
                    <FlatList
                        data={Object.values(comment.reviews)}
                        keyExtractor={(item) => item.textID.toString()}
                        renderItem={renderItem}
                        style={{ marginTop:20, backgroundColor:'#000' }} 
                    />
                    <Modal
                        animationType="slide"
                        transparent={true}
                        visible={isVisible}
                        onRequestClose={() => {
                            Alert.alert("Modal has been closed.");
                            setVisible(!isVisible);
                        }}
                        style
                    >
                        <View style={{ 
                        width:700,
                        height:hp(70),
                        backgroundColor:'#e0e0e0',
                        borderRadius:25,
                        position:'absolute',
                        right:30,
                        bottom:wp(-30),
                        justifyContent:'center',
                        alignItems:'center',
                    }} >
                            <View style={{ backgroundColor:'#fff', flexDirection:'row', width:wp(60), height: hp(15), fontSize:25, marginBottom:hp(3.5), borderRadius:10, alignItems:'center' }} >
                                <Text style={{ fontSize:16, fontWeight:'bold', marginHorizontal:10, alignSelf:'flex-start', marginTop:12 }} >旅程名稱:</Text>
                                <TextInput placeholder={placeholder} placeholderTextColor='#808080' onChangeText={setReText} multiline={true} numberOfLines={3} style={{ backgroundColor:'#fff', height: hp(14), width:wp(45), fontSize:20, borderRadius:10 }} underlineColor='transparent' activeUnderlineColor='#7ed957' />
                            </View>
                            <View>
                                <AirbnbRating
                                    ratingContainerStyle={{marginVertical:10,}}
                                    showRating
                                    onFinishRating={(rating) => {
                                        const rateStars = rating;
                                        setRateStars(rateStars);
                                    }}
                                    defaultRating={rateStars}
                                    
                                    
                                />
                            </View>
                            <View style={{ flexDirection:'row', alignItems:'center', justifyContent:'center', paddingTop:hp(15) }} >
                                <TouchableOpacity onPress={() => handleConfirm()} >
                                    <Text style={{ color:'#000', fontSize:30 }} >確定</Text>
                                </TouchableOpacity>

                                <TouchableOpacity
                                    onPress={() => {
                                        handleCancel()
                                    }}
                                    style={{ marginLeft:150 }}
                                    >
                                    <Text style={{ color:'#000', fontSize:30 }} >取消</Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                </Modal>
            </View>
        </SafeAreaView>


    );
};




const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor:"#000",
    },
    userInfoSection: {
        paddingHorizontal: 30,
        marginBottom: 25,
        backgroundColor:'#000'
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',

    },
    caption: {
        fontSize: 14,
        lineHeight: 14,
        fontWeight: '500',
    },
    row: {
        flexDirection: 'row',
        marginBottom: 10,
        marginLeft:45
    },
    infoBoxWrapper: {
        borderBottomColor: '#dddddd',
        borderBottomWidth: 1,
        borderTopColor: '#dddddd',
        borderTopWidth: 1,
        flexDirection: 'row',
        height: 100,
    },
    infoBox: {
        width: '50%',
        alignItems: 'center',
        justifyContent: 'center',
    },
    menuWrapper: {
        marginTop: 10,
    },
    menuItem: {
        flexDirection: 'row',
        paddingVertical: 15,
        paddingHorizontal: 30,
    },
    menuItemText: {
        color: '#fff',
        marginLeft: 20,
        fontWeight: '600',
        fontSize: 16,
        lineHeight: 26,
    },
    card:{
        marginLeft: 20,
        marginBottom: 10,
        width: 200,
        height: 150,
    },
    cardcontent:{
        alignItems: 'center',
        justifyContent:'center', 
        marginBottom: 20, 
    },
    cutline: {
        width: wp(100),
        height: 2,
        backgroundColor: '#fff',
        alignSelf: "center",
        marginVertical: 15,
    },

});