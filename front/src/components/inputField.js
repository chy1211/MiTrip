import { View, Text, TouchableOpacity, StyleSheet, TextInput } from "react-native";
import React from "react";

export default function InputField({label,
    icon,
    title,
    inputType,
    keyboardType,
    fieldButtonLabel,
    fieldButtonFunction,
    onChangeText,
    editable,
    secureTextEntry}){

    return(
      <View>
        <View >
          <Text style={{marginLeft:80,marginBottom:15,fontSize:18}}>
            {title}
          </Text>
        </View>
        <View style={styles.TextInput}>
        {icon}
        {inputType =='password' ? (
        <TextInput 
            placeholder={label}
            keyboardType={keyboardType}
            style={{flex: 1, paddingVertical: 0}}
            secureTextEntry={secureTextEntry}
            onChangeText={onChangeText}
        />) : (

        <TextInput 
            placeholder={label}
            keyboardType={keyboardType}
            style={{flex: 1, paddingVertical: 0}}
            onChangeText={onChangeText}
            editable={editable}
        />)}
        <TouchableOpacity onPress={fieldButtonFunction}>
          <Text style={{color:'#7ed957', fontWeight:'700'}}>
            {fieldButtonLabel}
            </Text>
        </TouchableOpacity>
      </View>
    </View>
    )
}


const styles=StyleSheet.create({

    TextInput: {
      flexDirection:'row',
      borderBottomColor:'#ccc',
      borderBottomWidth:1,
      alignSelf:'center',
      paddingBottom:8,
      marginBottom:25,
      width:600,
    },

    TextView: {
      marginBottom: 25,

    },
  })