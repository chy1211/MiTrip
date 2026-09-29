import React from "react";
import { Text, TouchableOpacity } from "react-native";
export default function CustomButton({label,onPress}){
    return(
        <TouchableOpacity onPress={onPress} 
                        style={{backgroundColor:'#7ed957',
                                padding:20,
                                borderRadius:10,
                                marginBottom:20,
                                alignSelf:'center',
                                width:500
                                }}>
            <Text style={{textAlign:'center',
                        fontWeight:'700',
                        fontSize: 18,
                        color:'#fff',
            }}>
            {label}
            </Text>
    </TouchableOpacity>
    )
}