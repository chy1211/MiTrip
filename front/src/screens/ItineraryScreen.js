import React, {useEffect, useState, useContext} from 'react';
import { SafeAreaView, ScrollView, View,TouchableOpacity, StyleSheet, Text, Switch } from 'react-native';
import { styles } from './styles'; // 引入你的 styles.js
import Litinerary from '../components/ltinerary';
import Ltineraryswitch from '../components/ltineraryswitch';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import Dialog from "react-native-dialog";
import DateTimePicker from '@react-native-community/datetimepicker'
import { Modal, TextInput } from 'react-native-paper';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import RNPickerSelect from 'react-native-picker-select';
import InputField from "../components/inputField";
import { useNavigation } from '@react-navigation/native';
import { AuthContext } from '../Context/AuthContext';
import ItineraryModal from '../components/ItineraryModal';
import { API_BASE_URL } from '../constants/config';

export default function ItineraryScreen() {
    const [activeCategory, setActiveCategory] = useState('我的旅程');
    const [visible, setVisible] = useState(false);
    const [name, setName] = useState("");
    const [sDescribe, setSDescribe] = useState("");
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [defaultStartDate, setDefaultStartDate] = useState(new Date());
    const [privilege, setPrivilege] = useState(0);
    const [stayTime, setStayTime] = useState([]);
    const [isEnabled, setIsEnabled] = useState(false);
    const [reData, setReData ] = useState([]);
    const navigation = useNavigation();
    const {userToken} = useContext(AuthContext);
    const [modalVisible, setModalVisible] = useState(false);
    const [scheduleData, setScheduleData] = useState([]);
    const [refetchData, setRefetchData] = useState(false);
    const {userID} = useContext(AuthContext);
    
    const handleToggleVisible = (newVisible) => {
        setModalVisible(newVisible);
    };

    const handleSetScheduleData = (data) => {
        setScheduleData(data);
    }
    console.log(scheduleData,'這是scheduleData')
    
    const checkTemp = (temp,word) => {
        if (temp !== '') {
            temp += '、';
        }
        temp += word;
        return temp;
    };
    

    const toggleSwitch = () => {
        setIsEnabled(previousState => !previousState);
        const valueToUse = isEnabled ? 0 : 1;
        setPrivilege(valueToUse);
    };
    

    const showDialog = () => {
        setVisible(true);
    };
    
    const handleCancel = () => {
        setVisible(false);
    };
    useEffect(() => {
        if (!startDate) {
            let today = new Date();
            const year = today.getFullYear();
            const month = today.getMonth() + 1; // 月份是從 0 開始的，所以要加 1
            const day = today.getDate();

            const formattedDate = `${year}-${month}-${day}`;
            // 轉換成字串並儲存
            setStartDate(formattedDate);
        }
      }, [name]); // 把startDate添加為useEffect的依賴
    
    const handleConfirm = async () => {
        // const startDateString = new Date(startDate);
        // startDateString.setDate(startDate.getDate() + stayTime);
        // const endDate = startDateString.toString().split('T')[0]
        // Do something with the input values
        setRefetchData(!refetchData);
        console.log('startDate初始值:',startDate);
        if (!startDate) {
            let today=new Date();
            const year = today.getFullYear();
            const month = today.getMonth() + 1; // 月份是從 0 開始的，所以要加 1
            const day = today.getDate();

            const formattedDate = `${year}-${month}-${day}`;
            //轉換成字串並儲存
            setStartDate(formattedDate);
        }
        const date = {
            "name": name,
            "sDescribe": sDescribe,
            "startDate": startDate,
            "endDate": endDate,
            "userID": userID,
            "privilege" : privilege,
        };
        // if (!validateInput(name, sDescribe, startDate, endDate, userID, privilege)) {
        //     return;
        // }
        try {

            console.log('取消')
            if (!name || !sDescribe || !startDate || !endDate) {
                let temp = '';

                !name && (temp += '旅程名稱、');
                !sDescribe && (temp = checkTemp(temp,'旅程描述'));
                !startDate && (temp = checkTemp(temp,'出發時間'));
                !endDate && (temp = checkTemp(temp,'停留天數'));

                alert(temp+'不得為空');
                return;
            }
            const response = await fetch(`${API_BASE_URL}/api/schedule/insert_data`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(date),
            });
        
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            setName("");
            setSDescribe("");
            setStartDate('');
            setEndDate('');
            setPrivilege(0);
            setVisible(false);
            const data = await response.json();

            return data; // 这里可能需要根据实际返回的数据结构进行调整
            } catch (error) {
            console.error('Error fetching distance and time:', error);
            // 如果请求失败，可以在这里处理错误情况
            setVisible(false);
        }
        
    }
    const refetchModalData = (data) => {
        setRefetchData(data);
        console.log(refetchData,'這是refetchData')
    }

    function validateInput(name, sDescribe, startDate, endDate, userID, privilege) {
        // 檢查所有欄位是否都已填寫
        if (!name || !sDescribe || !startDate || !endDate || !userID || !privilege) {
            alert('所有欄位都必須填寫');
            return false;
        }

        // 檢查日期是否是有效的日期
        if (isNaN(Date.parse(startDate)) || isNaN(Date.parse(endDate))) {
            alert('請輸入有效的日期');
            return false;
        }

        // 如果所有驗證都通過，則返回 true
        return true;
    }

    const handleDefaultDateChange = (data) => {
        
        const selectedDateTimestamp = data.nativeEvent.timestamp;
        const selectedDate = new Date(selectedDateTimestamp);
        console.log(selectedDate,'這是selectedDate')
        setDefaultStartDate(selectedDate)
        console.log(defaultStartDate,'這是defaultStartDate')


        const year = selectedDate.getFullYear();
        const month = selectedDate.getMonth() + 1; // 月份是從 0 開始的，所以要加 1
        const day = selectedDate.getDate();

        const formattedDate = `${year}-${month}-${day}`;
        //轉換成字串並儲存

            
        setStartDate(formattedDate)
        console.log(startDate,'這是startDate')
    }
            
    const numberOptions = Array.from({ length: 25 }, (_, index) => ({
        label: `${index + 1}`,
        value: index + 1,
    }));

    return (
        <View style={{flex:1}}>
            <View style={{position:"absolute",top:850,right:20,zIndex:1000}}>
                <ItineraryModal onVisibleChange={handleToggleVisible} visible={modalVisible}  scheduleData={scheduleData}  refetchData={refetchModalData}  refetchValue={refetchData}/>
            </View>
            <View style={{position:"absolute",top:850,right:20,zIndex:999,}}>
                
                <TouchableOpacity style={style1.absolute_look} onPress={showDialog}>
                    <MaterialIcons name="library-add" size={50} color='white' />
                </TouchableOpacity>
                <Modal 
                    visible={visible} 
                    animationType='slide'
                    transparent={true}
                >
                    <View style={{ 
                        width:700,
                        height:hp(70),
                        backgroundColor:'#e0e0e0',
                        borderRadius:25,
                        position:'absolute',
                        right:30,
                        bottom:30,
                        justifyContent:'center',
                        alignItems:'center',
                    }} >
                            <View style={{ backgroundColor:'#fff', flexDirection:'row', width:wp(60), height: hp(5), fontSize:25, marginBottom:hp(3.5), borderRadius:10, alignItems:'center' }} >
                                <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >旅程名稱:</Text>
                                <TextInput placeholder="請輸入名稱..." placeholderTextColor='#808080' onChangeText={setName} style={{ backgroundColor:'#fff', height: hp(5), width:wp(45), fontSize:20, borderRadius:10 }} underlineColor='transparent' activeUnderlineColor='#7ed957' />
                            </View>
                            <View style={{ backgroundColor:'#fff', width:wp(60), height: hp(5), fontSize:25, marginBottom:hp(3.5), borderRadius:10, alignItems:'center', flexDirection:'row' }} >
                                <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >旅程描述:</Text>
                                <TextInput placeholder="描述一下關於你的旅程吧..." placeholderTextColor='#808080' onChangeText={setSDescribe} style={{ backgroundColor:'#fff', height: hp(5), width:wp(45), fontSize:20, borderRadius:10 }} underlineColor='transparent' activeUnderlineColor='transparent' selectionColor='#7ed957' />
                            </View>
                            <View style={{ backgroundColor:'#fff', flexDirection:'row', width:wp(60), height:hp(25), alignItems:'center', marginBottom:hp(3.5), borderRadius:10 }} >
                                <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >出發時間:</Text>
                                <DateTimePicker
                                    mode='date'
                                    display='spinner'
                                    onChange={(data) => handleDefaultDateChange(data)}
                                    value={defaultStartDate}
                                    style={{ borderBottomWidth: 0}}
                                    
                                />
                            </View>
                            <View style={{ flexDirection:'row', alignItems:'center', backgroundColor:'#fff', width:wp(60), height: hp(5), borderRadius:10, marginBottom:hp(3.5) }} >
                                <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >遊玩天數:</Text>
                                <RNPickerSelect
                                    onValueChange={(value) => 
                                        {
                                            const newEndDate = new Date(defaultStartDate);
                                            newEndDate.setDate(defaultStartDate.getDate() + parseInt(value));
                                            setStayTime(value);
                                            const year = newEndDate.getFullYear();
                                            const month = newEndDate.getMonth() + 1; // 月份是從 0 開始的，所以要加 1
                                            const day = newEndDate.getDate();
                                            
                                            const formattedDate = `${year}-${month}-${day}`;
                                            //轉換成字串並儲存
                                            setEndDate(formattedDate);
                                            console.log(endDate,'這是endDate');
                                            
                                        }
                                    }
                                    textInputProps={{ style: { color:'#000', fontSize: 20, marginLeft:20} }}
                                    doneText='確定'
                                    placeholder={{ label: "請選擇遊玩天數", value: '', color: "#000" }}
                                    
                                    items={numberOptions}
                                    style={{inputIOS: { fontSize: 20, marginLeft:20, color:'#000' }, inputIOSContainer: { height: hp(5), width:wp(50), justifyContent:'center'}}}
                                />

                            </View>
                            
                            <View style={{ flexDirection:'row', alignItems:'center', backgroundColor:'#fff', width:wp(60), height: hp(5), borderRadius:10, marginBottom:hp(3.5) }}  >
                                <Text style={{ color:'#000', fontSize:16, fontWeight:'bold', marginRight:20, marginLeft:20 }} >是否公開行程:</Text>
                                <Switch
                                    trackColor={{ false: "#767577", true: "#7ed957" }}
                                    thumbColor={isEnabled ? "#f4f3f4" : "#f4f3f4"}
                                    ios_backgroundColor="#3e3e3e"
                                    onValueChange={toggleSwitch}
                                    value={isEnabled}
                                />
                            </View>

                            <View style={{ flexDirection:'row', alignItems:'center', justifyContent:'center' }} >
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
            <SafeAreaView style={[styles.safeAreaView, { backgroundColor: 'black' }]} >
                <View style={{marginTop:20, marginHorizontal:20}}>
                    <Ltineraryswitch activeCategory={activeCategory} setActiveCategory={setActiveCategory}/>
                </View>

                <ScrollView showsVerticalScrollIndicator={false} style={styles.scrollView}>
                    <View style={{marginTop: 20, alignSelf:'center'}}>

                        {activeCategory === '我的旅程' && (
                            <View>
                                <Litinerary onToggleVisible={handleToggleVisible} ModalData={handleSetScheduleData} refetchData={refetchData} />
                            </View>
                        )}
                        {activeCategory === '共同旅程' && (
                            <View>
                                <Litinerary />
                            </View>
                        )}
                    </View>
                    
                </ScrollView>
            </SafeAreaView>
        </View>
    );
}


const style1=StyleSheet.create({
    absolute_look:{
        height:80,
        width:80,
        backgroundColor:'#7ed957',
        borderRadius: 30,
        alignItems:'center',
        justifyContent: 'center',
    },
})