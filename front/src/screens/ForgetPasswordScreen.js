import React , {useState} from "react";
import {SafeAreaView, View, Text, TextInput, TouchableOpacity, StyleSheet,Image, Alert } from 'react-native';


//import SvgUri from 'react-native-svg';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import Icon from '@expo/vector-icons/Ionicons';

import InputField from "../components/inputField";
import CustomButton from "../components/CustomButton";
import fetchData from "../components/fetchData";


const ForgetPasswordScreen = ({navigation}) =>{

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');

  const handleButtonClick = async () => {
    //console.log('adasd');
    const response = await fetchData('ForgetPassword',
                                      username,
                                      '',
                                      '',
                                      email,
                                      '');

    // 檢查是否成功
    if (response && response.success) {
        // 在這裡你可以根據 responseData 做進一步的處理
        console.log(response.data);
        navigation.navigate('UpdatePassword',{username1:username});

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
      <View style={{paddingHorizontal:25}}>
      <View style={{alignItems: 'center'}}>
      {/* <RegistrationSVG width={300} 
                height={300} 
                style={{transform: [{rotate:'-5deg'}]}}
                /> */}
                
        <Image source={require('../../assets/images/MiTrip_LOGO_v2.png')} />
      </View>
      <Text style={{fontWeight:'500',
                    fontSize:40, 
                      color: '#333',
                      marginBottom:30,
                      alignSelf:'center'}}>
                        忘記密碼?
                      </Text>

      <InputField label={'您的帳號'} icon={<MaterialIcons
            name='person'
            size={30}
            color="#666"
            style={{marginRight:5}} 
            />}
            onChangeText={(text) => setUsername(text)} />

        <InputField label={'您的電子信箱'} icon={<MaterialIcons 
            name='email' 
            size={30} 
            color='#666'
            style={{marginRight:5}}/>}
            keyboardType={"email-address"}
            onChangeText={(text) => setEmail(text)} />

      <CustomButton label={'送出'} onPress={handleButtonClick}/>
      
      <View style={{flexDirection:'row', justifyContent:'center',marginBottom:30}}>
      {/* <Text style={{marginRight:5,fontWeight:'700',fontSize:18}}>已經註冊過了?</Text> */}
      <TouchableOpacity  onPress={() => {navigation.navigate('Login')}}>
      <Text style={{color:'#7ed957',fontWeight:'700',fontSize:18}}>點此返回</Text>
      </TouchableOpacity>
      </View>

      </View>
    </SafeAreaView>
  )
}



export default ForgetPasswordScreen


const styles=StyleSheet.create({

  SocialMediaSVG: {
    borderColor:'#ddd', 
    borderWidth:2, 
    borderRadius:10, 
    paddingHorizontal:30, 
    paddingVertical: 10,
  },
})