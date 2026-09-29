import React from "react";
import {View, Text,Button,StyleSheet, TouchableOpacity,TextInput,ImageBackground,Image, Platform } from 'react-native';

import Icon from '@expo/vector-icons/MaterialCommunityIcons';
import FontAwsome  from '@expo/vector-icons/FontAwesome';
import Feather from '@expo/vector-icons/Feather';
import { useTheme } from "react-native-paper";


const EditProfileScreen = () => {
    const {colors} = useTheme();
    return(
        <View style={styles.container}>
            <View style={{margin:20}}>
                <View style={{alignItems:'center'}}>
                    <TouchableOpacity onPress={() => {}}>
                        <View style={styles.ImageView}>
                            <ImageBackground
                                source={require('../../assets/images/user_avatar.png')}
                                style={{height:100,width:100}}
                                imageStyle={{borderRadius:15}}
                            >
                                <View style={{
                                    flex:1,
                                    justifyContent:'center',
                                    alignItems:'center',
                                }}>
                                    <Icon name='camera' size={35} color="#000" style={styles.CameraImage}></Icon>
                                </View>
                            </ImageBackground>
                            
                        </View>
                    </TouchableOpacity>
                    <Text style={{marginTop:5, fontSize:24, fontWeight:'bold'}}>Doge</Text>
                </View>
                <View style={styles.action}>
                    <Feather name="user" color={colors.text} size={20}/>
                    <TextInput
                        placeholder="暱稱"
                        style={styles.textInput}
                    />
                </View>
                <View style={styles.action}>
                    <Feather name="phone" color={colors.text} size={20}/>
                    <TextInput
                        placeholder="聯絡電話"
                        keyboardType="number-pad"
                        style={styles.textInput}
                    />
                </View>
                <View style={styles.action}>
                    <Feather name="mail" color={colors.text}  size={20}/>
                    <TextInput
                        placeholder="信箱"
                        style={styles.textInput}
                    />
                </View>
                <View style={styles.action}>
                    <Feather name="globe" color={colors.text}  size={20}/>
                    <TextInput
                        placeholder="國家"
                        style={styles.textInput}
                    />
                </View>
                <View style={styles.action}>
                    <Feather name="map-pin" color={colors.text}  size={20}/>
                    <TextInput
                        placeholder="城市"
                        style={styles.textInput}
                    />
                </View>
                <TouchableOpacity style={styles.commandButton} onPress={() => {}}>
                      <Text style={styles.panelButtonTitle}>更改</Text>
                </TouchableOpacity>
            </View>
        </View>

    );
};


export default EditProfileScreen;


const styles = StyleSheet.create({
    container: {
      flex: 1,
    },
    ImageView:{
        height:100,
        width:100,
        borderRadius:15,
        justifyContent:'center',
        alignItems:'center',
    },
    CameraImage:{
        opacity:0.6,
        alignItems:'center',
        justifyContent:'center',
        borderWidth:1,
        borderColor:'#fff',
        borderRadius: 10,
    },
    commandButton: {
      padding: 15,
      borderRadius: 10,
      backgroundColor: '#FF6347',
      alignItems: 'center',
      marginTop: 10,
    },
    panel: {
      padding: 20,
      backgroundColor: '#FFFFFF',
      paddingTop: 20,
      // borderTopLeftRadius: 20,
      // borderTopRightRadius: 20,
      // shadowColor: '#000000',
      // shadowOffset: {width: 0, height: 0},
      // shadowRadius: 5,
      // shadowOpacity: 0.4,
    },
    header: {
      backgroundColor: '#FFFFFF',
      shadowColor: '#333333',
      shadowOffset: {width: -1, height: -3},
      shadowRadius: 2,
      shadowOpacity: 0.4,
      // elevation: 5,
      paddingTop: 20,
      borderTopLeftRadius: 20,
      borderTopRightRadius: 20,
    },
    panelHeader: {
      alignItems: 'center',
    },
    panelHandle: {
      width: 40,
      height: 8,
      borderRadius: 4,
      backgroundColor: '#00000040',
      marginBottom: 10,
    },
    panelTitle: {
      fontSize: 27,
      height: 35,
    },
    panelSubtitle: {
      fontSize: 14,
      color: 'gray',
      height: 30,
      marginBottom: 10,
    },
    panelButton: {
      padding: 13,
      borderRadius: 10,
      backgroundColor: '#FF6347',
      alignItems: 'center',
      marginVertical: 7,
    },
    panelButtonTitle: {
      fontSize: 17,
      fontWeight: 'bold',
      color: 'white',
    },
    action: {
      flexDirection: 'row',
      marginTop: 10,
      marginBottom: 10,
      borderBottomWidth: 1,
    //   borderBottomColor: '#f2f2f2',
      borderBottomColor:'gray',
      paddingBottom: 5,
    },
    actionError: {
      flexDirection: 'row',
      marginTop: 10,
      borderBottomWidth: 1,
      borderBottomColor: '#FF0000',
      paddingBottom: 5,
    },
    textInput: {
      flex: 1,
      marginTop: Platform.OS === 'ios' ? 0 : -5,
      paddingLeft: 10,
      color: '#05375a',
      placeholderTextColor:"#666666",
        autoCorrect:false,
    },
  });
  