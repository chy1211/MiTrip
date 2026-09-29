import React , {useState} from "react";
import {SafeAreaView, View, Text, TextInput, TouchableOpacity, StyleSheet, Platform, ToastAndroid,Image, Alert } from 'react-native';


//import SvgUri from 'react-native-svg';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import Icon from '@expo/vector-icons/Ionicons';
import DateTimePicker from '@react-native-community/datetimepicker';

import InputField from "../components/inputField";
import CustomButton from "../components/CustomButton";
import fetchData from "../components/fetchData";


const RegisterScreen = ({navigation}) =>{

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [checkPassword, setCheckPassword] = useState('');
  const [email, setEmail] = useState('');
  const [birthDay, setBirthDay] = useState('2023-11-25');

  const [date, setDate] = useState(new Date());
  const [show, setShow] = useState(false);
  const [mode, setMode] = useState('date');

  const [passwordVisible,setPasswordVisible] = useState(false);
  const [passwordVisible2,setPasswordVisible2] = useState(false);


  const onChange = ({type}, selectedDate) => {
    const currentDate = selectedDate || date;
    setShow(Platform.OS === 'ios');
    setDate(currentDate);

    let tempDate = new Date(currentDate);
    let fDate = tempDate.getFullYear() + '-' + (tempDate.getMonth() + 1) + '-' + tempDate.getDate();
    setBirthDay(fDate);
    console.log(fDate);
  };
  const PasswordVisibleChange =() =>{
    setPasswordVisible(!passwordVisible);
    console.log('PasswordVisible=',passwordVisible);
  }
  const PasswordVisibleChange2 =() =>{
    setPasswordVisible2(!passwordVisible2);
    console.log('PasswordVisible2=',passwordVisible2);
  }

  const showMode = (currentMode) => {
    setShow(true);
    setMode(currentMode);
  };
  const handleButtonClick = async () => {
    //console.log('adasd');
    const response = await fetchData(
                                      'Register',
                                      username,
                                      password,
                                      checkPassword,
                                      email,
                                      birthDay);

    // 檢查是否成功
    if (response && response.success) {
        // 在這裡你可以根據 responseData 做進一步的處理
        console.log(response.data);
        navigation.navigate('Login');

    } else {
        // 如果有錯誤，顯示警告
        if (response && response.error) Alert.alert('Error', response.error);
    }
  };

  return(
    <SafeAreaView style={{flex:1, justifyContent:'center'}}>
      <TouchableOpacity 
        style={{position:'absolute', left:10,top:50,zIndex:10}}
        onPress={() => navigation.navigate('Login')}
        >
          <View style={{flexDirection:'row',alignItems:'center'}}>
            <Icon name="arrow-undo" size={30} color={'gray'}/>
            <Text style={{marginLeft:3}}>返回</Text>
          </View>
        </TouchableOpacity>
        
      <View style={{paddingHorizontal:25,}}>
      <View style={{alignItems: 'center',height:300,marginBottom:100}}>
      <Image source={require('../../assets/images/MiTrip_LOGO_v2.png')} />
                
      </View>
      {/* <Text style={{fontWeight:'500',
                    fontSize:40, 
                      color: '#333',
                      marginBottom:30,
                      alignSelf:'center'}}>
                        註冊
                      </Text> */}

      <InputField label={'輸入您的帳號'} icon={<MaterialIcons
            name='person'
            size={30}
            color="#666"
            style={{marginRight:5}} 
            />}
            title='您的帳號'
            onChangeText={(text) => setUsername(text)} />

        <InputField label={'輸入您的密碼'} icon={<Icon
            name='lock-closed-outline' 
            size={30} 
            color='#666'
            style={{marginRight:5}}/>}
            title='您的密碼'
            inputType='password'
            secureTextEntry={passwordVisible}
            fieldButtonLabel={'顯示密碼'}
            fieldButtonFunction={() =>PasswordVisibleChange()}
            onChangeText={(text) => setPassword(text)}
            />
        <InputField label={'再次輸入您的密碼'} icon={<Icon
            name='lock-closed-sharp' 
            size={30} 
            color='#666'
            style={{marginRight:5}}/>}
            title='確認您的密碼'
            inputType='password'
            secureTextEntry={passwordVisible2}
            fieldButtonLabel={'顯示密碼'}
            fieldButtonFunction={() =>PasswordVisibleChange2()}
            onChangeText={(text) => setCheckPassword(text)}
            />

        <InputField label={'輸入您的電子信箱'} icon={<MaterialIcons 
            name='email' 
            size={30} 
            color='#666'
            style={{marginRight:5}}/>}
            title='您的電子信箱'
            keyboardType={"email-address"}
            onChangeText={(text) => setEmail(text)} />

        <TouchableOpacity onPress={() => {showMode('date')}}>
          <InputField label={`${birthDay}`} icon={<MaterialIcons 
              name='calendar-today' 
              size={30} 
              color='#666'
              style={{marginRight:5}}/>}
              title='您的生日'
              editable={false}
              onChangeText={(text) => setBirthDay(text)} />
        </TouchableOpacity>

        {show && (
          <DateTimePicker
          mode = 'date'
          display = "calender"
          label= '您的生日'
          value = {date}
          onChange={onChange}
          maximumDate = {new Date()}
        />
        )}
        

        
    <CustomButton label={'註冊'} onPress={() => {handleButtonClick()}}/>

      <Text style={{textAlign:'center', color:'#666', marginBottom:30}}>
        或者...
      </Text>

    
      <View style={{flexDirection:'row', justifyContent:'center',marginBottom:30}}>
      <Text style={{marginRight:5,fontWeight:'700',fontSize:18}}>已經註冊過了?</Text>
      <TouchableOpacity  onPress={() => {navigation.navigate('Login')}}>
      <Text style={{color:'#7ed957',fontWeight:'700',fontSize:18}}>點此登入</Text>
      </TouchableOpacity>
      </View>

      </View>
    </SafeAreaView>
  )
}



export default RegisterScreen


const styles=StyleSheet.create({

  SocialMediaSVG: {
    borderColor:'#ddd', 
    borderWidth:2, 
    borderRadius:10, 
    paddingHorizontal:30, 
    paddingVertical: 10,
  },
})