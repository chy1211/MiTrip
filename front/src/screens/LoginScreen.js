import React , { useState, useContext } from "react";
import {SafeAreaView, View, Text, TextInput, TouchableOpacity, StyleSheet, Image} from 'react-native';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import Icon from '@expo/vector-icons/Ionicons';
import InputField from "../components/inputField";
import CustomButton from "../components/CustomButton";
import { AuthContext } from "../Context/AuthContext";

const LoginScreen = ({navigation}) =>{

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(true);

  const {login} = useContext(AuthContext);
  
  const handleLogin = async () => {
    const response = await login('Login', username, password);
    if (response != 'error') {
      navigation.navigate('Home');
    }else{
      navigation.navigate('Login');
    }
  };

  const PasswordVisibleChange =() =>{
    setPasswordVisible(!passwordVisible);
    console.log('PasswordVisible=',passwordVisible);
  }
  
  return(
    <SafeAreaView style={{flex:1, justifyContent:'center'}}>
      <TouchableOpacity 
        style={{position:'absolute', left:10,top:50,zIndex:10,}}
        onPress={() => navigation.goBack()}
        >
          <View style={{flexDirection:'row',alignItems:'center'}}>
            <Icon name="arrow-undo" size={30} color={'gray'}/>
            <Text style={{marginLeft:3}}>返回</Text>
          </View>
        </TouchableOpacity>
      <View style={{paddingHorizontal:25}}>
        
      <View style={{alignItems: 'center'}}>
      <Image source={require('../../assets/images/MiTrip_LOGO_v2.png')} />
                
      </View>
      <Text style={{fontWeight:'500',
                    fontSize:40, 
                      color: '#333',
                      marginBottom:30,
                      alignSelf:'center'}}>
                        歡迎回來
                      </Text>

      <InputField label={'您的帳號'} icon={<MaterialIcons 
            name='person' 
            size={30} 
            color='#666'
            style={{marginRight:5}}/>}
            onChangeText={(text) => setUsername(text)} // 更新 username 状态
            />
      
      <InputField label={'您的密碼'} icon={<Icon
            name='lock-closed-outline' 
            size={30} 
            color='#666'
            style={{marginRight:5}}/>}
            inputType='password'
            secureTextEntry={passwordVisible}
            fieldButtonLabel={'顯示密碼'}
            fieldButtonFunction={() =>PasswordVisibleChange()}
            onChangeText={(text) => setPassword(text)} // 更新 password 状态
            />


      {/* <CustomButton label={'登入'} onPress={() => {fetchData(option='Login',
                                                            username1=username,
                                                            password1=password)}}/> */}
      <CustomButton label={'登入'} onPress={() => handleLogin()}/>

      <TouchableOpacity onPress={() => navigation.navigate('ForgetPassword')}>
        <Text style={{textAlign:'center', color:'#666', marginBottom:30,fontSize:18}}>
          忘記密碼?
        </Text>
      </TouchableOpacity>

      <View style={{flexDirection:'row', justifyContent:'center',marginBottom:30}}>
      <Text style={{marginRight:5,fontWeight:'700',fontSize:18}}>還不是會員?</Text>
      <TouchableOpacity  onPress={() => {navigation.navigate('Register')}}>
      <Text style={{color:'#7ed957',fontWeight:'700',fontSize:18}}>點此註冊</Text>
      </TouchableOpacity>
      </View>

      </View>
    </SafeAreaView>
  )
}



export default LoginScreen


const styles=StyleSheet.create({

  SocialMediaSVG: {
    borderColor:'#ddd', 
    borderWidth:2, 
    borderRadius:10, 
    paddingHorizontal:30, 
    paddingVertical: 10,
  },
})