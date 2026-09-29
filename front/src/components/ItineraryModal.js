import React, {useEffect, useState, useContext, useRef} from 'react';

import { SafeAreaView, ScrollView, View,TouchableOpacity, StyleSheet, Text, Switch } from 'react-native';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import DateTimePicker from '@react-native-community/datetimepicker'
import { Modal, TextInput, Portal, PaperProvider  } from 'react-native-paper';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import RNPickerSelect from 'react-native-picker-select';
import { useNavigation } from '@react-navigation/native';
import { AuthContext } from '../Context/AuthContext';
import { API_BASE_URL } from '../constants/config';

export default function ItineraryModal({onVisibleChange,visible, scheduleData, refetchData, refetchValue}) {
    const scheduleDataIn = scheduleData;
    console.log(scheduleDataIn,'這是scheduleData，Modal')
    const [name, setName] = useState('');
    const [sDescribe, setSDescribe] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [defaultStartDate, setDefaultStartDate] = useState(new Date());
    const [privilege, setPrivilege] = useState(0);
    const [stayTime, setStayTime] = useState(null);
    const [isEnabled, setIsEnabled] = useState(false);
    const navigation = useNavigation();
    const {userToken} = useContext(AuthContext);
    const {userID} = useContext(AuthContext);
    const showStayTime = stayTime
    const Ref = useRef();

    useEffect(() => {
        if (scheduleDataIn === undefined ) return;
        setStartDate(scheduleDataIn.startDate);
        setName(scheduleDataIn.name);
        setSDescribe(scheduleDataIn.sDescribe);
        setStayTime(scheduleDataIn.days);
        setEndDate(scheduleDataIn.endDate);
        setPrivilege(scheduleDataIn.privilege);
        setDefaultStartDate(new Date(scheduleDataIn.startDate));
    },[scheduleDataIn])

    useEffect(() => {
            console.log('這是Ref.current')
            const newEndDate = new Date(defaultStartDate);
            newEndDate.setDate(defaultStartDate.getDate() + parseInt(scheduleDataIn.days) - 1 );
            const year = newEndDate.getFullYear();
            const month = newEndDate.getMonth() + 1; // 月份是從 0 開始的，所以要加 1
            const day = newEndDate.getDate();
            
            const formattedDate = `${year}-${month}-${day}`;
            //轉換成字串並儲存
            setEndDate(formattedDate);
    },[startDate])


    useEffect(() => {
        if ( privilege === 0){
            setIsEnabled(false);
        }else{
            setIsEnabled(true);
        }
    },[privilege])

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
        console.log(valueToUse,'這是privilege')
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
        // Do something with the input values
        console.log(name, sDescribe, startDate, stayTime);

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

                !name && (temp += '旅程名稱');
                !sDescribe && (temp = checkTemp(temp,'旅程描述'));
                !startDate && (temp = checkTemp(temp,'出發時間'));
                !endDate && (temp = checkTemp(temp,'停留天數'));

                alert(temp+'不得為空');
                return;
            }
            const response = await fetch(`${API_BASE_URL}/api/schedule/update_schedule/${scheduleDataIn.scheduleID}`, {
                method: 'PUT',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(date),
            });
        
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            onVisibleChange(false);
            setName(scheduleDataIn.name);
            setSDescribe(scheduleDataIn.sDescribe);
            setStartDate(scheduleDataIn.startDate);
            setEndDate(scheduleDataIn.endDate);
            setPrivilege(scheduleDataIn.privilege);
            setStayTime(scheduleDataIn.days);
            const data = await response.json();
            console.log(data,'這是data')
            onVisibleChange(false);
            console.log(refetchValue,'這是refetchValue');
            refetchData(!refetchValue);
            return data; // 这里可能需要根据实际返回的数据结构进行调整
            } catch (error) {
            console.error('Error fetching distance and time:', error);
            // 如果请求失败，可以在这里处理错误情况
            onVisibleChange(false);
        }
        
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
            
    const numberOptions = Array.from({ length: 30 }, (_, index) => ({
        label: `${index + 2}`,
        value: index + 2,
    }));

    useEffect(() => {
        console.log(stayTime,'這是stayTime')
    },[stayTime])


    return(
        <PaperProvider>
            <Portal>
                <Modal 
                            visible={visible} 
                            animationType='slide'
                            transparent={true}
                            onDismiss={() =>{
                                console.log('I Click OutSide');
                                onVisibleChange(false);
                                
                            }}
                            overlayAccessibilityLabel='close your screen'
                            
                        >
                            <View 
                            style={{ 
                                flex:1,
                                width:700,
                                height:hp(70),
                                backgroundColor:'#e0e0e0',
                                borderRadius:25,
                                position:'absolute',
                                right:30,
                                bottom:0,
                                justifyContent:'center',
                                alignItems:'center',
                                elevation: 9999 ,
                                zIndex: 9999,
                            }} 
                            >
                                    <View style={{ backgroundColor:'#fff', flexDirection:'row', width:wp(60), height: hp(5), fontSize:25, marginBottom:hp(3.5), borderRadius:10, alignItems:'center' }} >
                                        <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >旅程名稱:</Text>
                                        <TextInput placeholder={scheduleDataIn.name} placeholderTextColor='#808080' onChangeText={setName} style={{ backgroundColor:'#fff', height: hp(5), width:wp(45), fontSize:20, borderRadius:10 }} underlineColor='transparent' activeUnderlineColor='#7ed957' />
                                    </View>
                                    <View style={{ backgroundColor:'#fff', width:wp(60), height: hp(5), fontSize:25, marginBottom:hp(3.5), borderRadius:10, alignItems:'center', flexDirection:'row' }} >
                                        <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >旅程描述:</Text>
                                        <TextInput placeholder={scheduleDataIn.sDescribe} placeholderTextColor='#808080' onChangeText={setSDescribe} style={{ backgroundColor:'#fff', height: hp(5), width:wp(45), fontSize:20, borderRadius:10 }} underlineColor='transparent' activeUnderlineColor='transparent' selectionColor='#7ed957' />
                                    </View>
                                    <View style={{ backgroundColor:'#fff', flexDirection:'row', width:wp(60), height:hp(25), alignItems:'center', marginBottom:hp(3.5), borderRadius:10 }} >
                                        <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >出發時間:</Text>
                                        <DateTimePicker
                                            mode='date'
                                            display='spinner'
                                            onChange={(data) => handleDefaultDateChange(data)}
                                            value={new Date(scheduleDataIn.startDate)}
                                            style={{ borderBottomWidth: 0}}
                                            
                                        />
                                    </View>
                                    <View style={{ flexDirection:'row', alignItems:'center', backgroundColor:'#fff', width:wp(60), height: hp(5), borderRadius:10, marginBottom:hp(3.5) }} >
                                        <Text style={{ fontSize:16, fontWeight:'bold', marginLeft:20 }} >停留天數:</Text>
                                        <RNPickerSelect
                                            onValueChange={(value) => 
                                                {
                                                    const newEndDate = new Date(defaultStartDate);
                                                    newEndDate.setDate(defaultStartDate.getDate() + parseInt(value) - 1);
                                                    setStayTime(value);
                                                    const year = newEndDate.getFullYear();
                                                    const month = newEndDate.getMonth() + 1; // 月份是從 0 開始的，所以要加 1
                                                    const day = newEndDate.getDate();
                                                    
                                                    const formattedDate = `${year}-${month}-${day}`;
                                                    //轉換成字串並儲存
                                                    setEndDate(formattedDate);
                                                    console.log(value,'這是value')
                                                }
                                            }
                                            textInputProps={{ style: { color:'#000', fontSize: 20, marginLeft:20} }}
                                            doneText='確定'
                                            placeholder={{ label: `${showStayTime}`, value: showStayTime, color: "#000" }}
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
                                                onVisibleChange(false);
                                                setName(scheduleDataIn.name);
                                                setSDescribe(scheduleDataIn.sDescribe);
                                                setStartDate(scheduleDataIn.startDate);
                                                setEndDate(scheduleDataIn.endDate);
                                                setPrivilege(scheduleDataIn.privilege);
                                                setStayTime(scheduleDataIn.days);
                                            }}
                                            style={{ marginLeft:150 }}
                                            >
                                            <Text style={{ color:'#000', fontSize:30 }} >取消</Text>
                                        </TouchableOpacity>
                                    </View>
                            </View>
                        </Modal>
                    </Portal>
                </PaperProvider>
    )
}





