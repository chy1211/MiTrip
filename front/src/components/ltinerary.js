import { View, Text, TouchableOpacity, Image, ScrollView, StyleSheet, TextInput, SafeAreaView, Switch } from 'react-native'
import React, { useState, useEffect, useContext } from 'react'
import { categoriesData, destinationData } from '../constants'
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { LinearGradient } from 'expo-linear-gradient'
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons as IconM, Ionicons as IconI } from '@expo/vector-icons';
import { Modal } from 'react-native-paper';
import RNPickerSelect from 'react-native-picker-select';
import DateTimePicker from '@react-native-community/datetimepicker';
import ItineraryModal from './ItineraryModal';
import { AuthContext } from '../Context/AuthContext';
import { API_BASE_URL } from '../constants/config';

export default function itinerary({ activeLitinerary, Litinerary, onToggleVisible, ModalData, refetchData }) {
    const navigation = useNavigation();
    const [scheduleData, setScheduleData] = useState([]);
    const [modalVisible, setModalVisible] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [isDelete, setIsDelete] = useState(false);
    const {userID} = useContext(AuthContext);
    const handleModal = (newVisible) =>{

        setModalVisible(newVisible);
        console.log('this is outside',newVisible);
    }

    const fetchData = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/schedule/select_by_user_id/${userID}`);
            const data = await response.json();

        // 更新组件状态，显示获取到的详细信息
            setScheduleData(data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        fetchData();
        console.log('refetchData',refetchData);
    }, [refetchData]);

    const categoriesDataObject = Object.fromEntries(categoriesData.map((category, index) => [index, category]));
    return (
        
        <SafeAreaView style={{flex:1}}>
        
            <View style={{ flex: 1, paddingHorizontal: wp(6) }}>
                
                <ScrollView  contentContainerStyle={{ flexDirection: 'column', alignItems:'center', justifyContent: 'center', paddingVertical: hp(2), width: wp(80) }} contentOffset={{ x: 280, y: 0 }} style={{ flex: 1 }}>
                    {
                        Object.values(scheduleData).map((item, index) => (
                            <DestinationCard navigation={navigation} item={item} index={index} key={index} categoriesDataObject={categoriesDataObject} onToggleVisible={onToggleVisible} ModalData={ModalData} refetchData={fetchData} />
                        ))
                    }
                </ScrollView>
            </View>
            {/* <ItineraryModal onVisibleChange={handleModal} visible={modalVisible} /> */}
        </SafeAreaView>
    )
}

const DestinationCard = ({ item, navigation, index, categoriesDataObject, onToggleVisible, ModalData, refetchData }) => {
    const [isEditable, setIsEditable] = useState(false);
    const [visible, setVisible] = useState(false);

    


    const handleModal = (newVisible) => {
        setVisible(newVisible);
        // 调用通过 props 传递过来的函数
        onToggleVisible(newVisible);
        console.log('按下編輯',newVisible);
        console.log('Visible:',visible);
        console.log('onToggleVisible:',onToggleVisible);
        
    };
    
    const showEdit = (item) => {
        setIsEditable(!isEditable);
        console.log('showEdit_________',isEditable);
        ModalData(item);
    }
    const handleDelete = async (item) => {
        // 這裡做刪除資料
        console.log('handleDelete',item);
        try{
            const response = await fetch(`${API_BASE_URL}/api/schedule/delete_schedule/${item.scheduleID}`, {
                method: 'DELETE',
                headers: {
                'Content-Type': 'application/json',
                },
            });
        
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            
            const data = await response.json();
            console.log('data',data);
            await refetchData();

            return data; // 这里可能需要根据实际返回的数据结构进行调整
        } catch (error) {
            console.error('Error Delete schedule:', error);

        }
        
    };

    return (
        <SafeAreaView style={styles.container}>
            <TouchableOpacity onPress={()=> navigation.navigate('Edit', {...item})} style={{ flexDirection:'column',position: 'relative', marginBottom:30 }}>                
                <Image source={categoriesDataObject[index].image} style={{ width: wp(60), height: hp(30), borderRadius: 8 }} />
                <LinearGradient 
                    colors={['transparent', 'rgba(0,0,0,0.8)']}
                    style={{ position: 'absolute', width: wp(60), height: hp(10), borderRadius: 8, top: hp(30) - hp(30) }}
                    start={{ x: 0.5, y: 1 }}
                    end={{ x: 0.5, y: -0.5 }}                    
                />
                <LinearGradient 
                    colors={['transparent', 'rgba(0,0,0,0.8)']}
                    style={{ position: 'absolute', width: wp(60), height: hp(10), borderRadius: 8, top: hp(30)-hp(10) }}
                    start={{ x: 0.5, y: 0 }}
                    end={{ x: 0.5, y: 0.5 }}                
                />
                <TouchableOpacity style={{ position: 'absolute', top: 0, right:0, width:50, height:50, alignItems:'center' }} onPress={() => showEdit(item)} >
                    <IconI name='ellipsis-horizontal' size={30} color='white'  />
                    <Modal 
                        visible={isEditable}
                        onDismiss={() =>setIsEditable(false)}
                        transparent={true}
                    >
                        <View 
                            style={{ 
                                width:wp(20),
                                height:hp(10),
                                backgroundColor:'#e0e0e0',
                                borderRadius:10,
                                position:'absolute',
                                right:10,
                                top:0,
                                justifyContent:'center',
                                
                                
                            }}
                        >
                            <TouchableOpacity onPress={() => {handleModal(true)}} style={{ justifyContent:'center', alignItems:'center' }} >
                                <Text style={{ fontSize:20, marginTop:10, marginBottom:10 }}>編輯</Text>
                                <View style={{ width: wp(20), height: 2, backgroundColor: '#fff', alignSelf: "center" }} />
                            </TouchableOpacity>
                            <TouchableOpacity onPress={() => handleDelete(item)} style={{ justifyContent:'center', alignItems:'center' }} >
                                <Text style={{ fontSize:20, marginTop:10, marginBottom:10 }}>刪除</Text>
                            </TouchableOpacity>

                        </View>
                    </Modal>
                </TouchableOpacity>
                
                <Text style={{ color: 'white', position:'absolute', top:hp(25), fontSize:20, marginLeft:15 }}>{item.name}</Text>
                <Text style={{ color: 'white', position:'absolute', top:hp(27), fontSize:15, marginLeft:15 }}>{item.startDate}~{item.endDate}</Text>
            </TouchableOpacity>
        </SafeAreaView>

    )
}



const styles = StyleSheet.create ({
    container:{
        flex:1,
        flexDirection:'column',
        
    },
    headerContainer:{
        flex:1,
        flexDirection:'row',
        backgroundColor:'white',
        justifyContent:'center',
        width: wp(70),
    },
    textContainer: { // 占据剩余的空间
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection:'row',
    },
    ContentContainer:{
        flex: 1, // 指定中间区域占比为 2
        justifyContent: 'center',
    },
    headingText:{
        fontSize: 28,
        fontWeight: 'bold',
        color:'black',
        textAlign:'center',

    },
    Edit:{
        marginRight:10,
        flexDirection:'row',
    },
    cardButton:{
        justifyContent:'flex-end',
        padding: 10,
        borderWidth: 1,
        borderRadius: 30,
        borderColor: 'gray',
        backgroundColor: 'gray',
    },
    cardElevated:{},
    cardImage:{ 
        width:  wp(70),
        height: hp(25),
        borderTopLeftRadius: 25,
        borderTopRightRadius: 25,
            },
    cardBody:{
        flex: 1,
        flexDirection:'row',
        backgroundColor:'white',
        height: 90,
        borderBottomLeftRadius: 25,
        borderBottomRightRadius: 25,
        marginBottom: 50,
        
    },
    cardLabel:{
        fontSize: 20,
        marginLeft:15,
        textAlign:'left',
        
    },


})