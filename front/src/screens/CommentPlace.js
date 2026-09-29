import React, { useState, useEffect, useContext } from "react";
import {View, Text, TouchableOpacity, TextInput, StyleSheet, SafeAreaView, Modal, Alert } from 'react-native';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { Ionicons as Iconi, FontAwesome as IconF, AntDesign as Icona, MaterialCommunityIcons as IconM  } from '@expo/vector-icons';
import { Rating, AirbnbRating } from "react-native-ratings";
import InputField from "../components/inputField";
import fetchData from "../components/fetchData";
import { AuthContext } from "../Context/AuthContext";

const FloatScreen = React.memo(({ isVisible, onClose, onRatingChange, restaurantName, restaurantId, userid, dataType  }) => {
    const [postComment, setPostComment] = useState("");
    const [rateStars, setRateStars] = useState(0);
    const onSubmit = async () => {
        const response = await fetchData(
            'PostComment',
            '',
            '',
            '',
            '',
            '',
            restaurantId,
            userid,
            postComment,
            rateStars,
            '',
            dataType,
        );
    
        // 檢查是否成功
        if (response && response.success) {
            console.log(response.data);
            onClose();
        } else {
            if (response && response.error) Alert.alert('Error', response.error);
        }
    };

    return (
        <Modal
            visible={isVisible}
            animationType="none"
            transparent={true}
            style={{ justifyContent: "center", alignItems: "center" }}
        >
        <View style={styles.container}>
            <Text style={styles.title}>{restaurantName}</Text>
            <View>
                <AirbnbRating
                    ratingContainerStyle={{marginVertical:10,}}
                    showRating
                    onFinishRating={(rating) => {
                            const rateStars = rating;
                            setRateStars(rateStars);
                            }}
                    />
            </View>
            <View style={{ width: "80%" }}>
                <TextInput
                style={styles.input}
                placeholder="評論在此"
                multiline={true}
                onChangeText={(text) => setPostComment(text)}
                />
            </View>
            <TouchableOpacity style={styles.submitButton} onPress={onSubmit}>
                <Text style={styles.submitButtonText}>提交</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.closeButton} onPress={onClose}>
                <Text style={styles.closeButtonText}>關閉</Text>
            </TouchableOpacity>
            </View>
        </Modal>
    );
});

export default function CommentPlace({ restaurantName, restaurantId, OnPressChange, dataType = 'restaurant' }) {
    const [isModalVisible, setModalVisible] = useState(false);
    const [rateStars, setRateStars] = useState(0);
    const [onPressHandle, setOnPressHandle] = useState(false);
    const {userID} = useContext(AuthContext);
    const handleSubmission = () => {
        // 执行提交评论的逻辑

        // 清空评论框
        

        // 关闭浮动视窗
        setModalVisible(false);
    };

    const handleRatingChange = (rating) => {
        console.log("rating", rating);
        setRateStars(rating);
        OnPressChange(!rateStars);
    };

    const toggleVisible = () => {
        setModalVisible(!isModalVisible);
        setOnPressHandle(!onPressHandle);
        OnPressChange(!onPressHandle);

    };

    return (
        <View>
            <TouchableOpacity style={styles.buttonStyle} onPress={toggleVisible}>
                <IconM name="comment-edit-outline" size={26} color={"white"} />
                <Text style={styles.buttontext}>撰寫評論</Text>
            </TouchableOpacity>

            <FloatScreen
                isVisible={isModalVisible}
                onClose={() => setModalVisible(false)}
                onRatingChange={handleRatingChange}
                restaurantName={restaurantName}
                restaurantId={restaurantId}
                userid={userID}
                dataType={dataType}
            />
        </View>
    );
}


const styles = StyleSheet.create({
    buttontext:{
        fontSize:16,
        color:'white',
        fontWeight:'700',
        fontFamily:'',
        padding:5,
    },
    buttonStyle:{
        flexDirection:'row',
        backgroundColor:'#7ed957',
        borderRadius:25,
        padding:10,
        borderWidth:2,
        borderColor:'#c0c0c0',
        justifyContent:'center',
        alignItems:'center',
    },
    Card:{
        flex:1,
        flexDirection:'row',
        alignItems:'center',
        borderBottomWidth:0.5,
        borderColor:'silver',
        marginBottom:15,
    },
    CardImg:{
        borderWidth:1,
        borderRadius:50,
        width:60,
        height:60,
        justifyContent:'center',
        alignItems:'center',
        backgroundColor:'gray',
    },
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        alignSelf:'center',
        padding: 20,
        width:500,
        height:400,
        backgroundColor:'white',
        padding: 20,
        marginVertical:300,
        borderWidth:2,
        borderColor:'silver',
        borderRadius:25,
        },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    input: {
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 5,
        padding: 10,
        height: 100,
        marginBottom: 20,
        width: '100%',
    },
    submitButton: {
        backgroundColor: '#7ed957',
        padding: 10,
        borderRadius: 5,
        width: '100%',
        alignItems: 'center',
    },
    submitButtonText: {
        color: 'white',
        fontSize: 18,
    },
    closeButton: {
        marginTop: 10,
        padding: 10,
    },
    closeButtonText: {
        color: 'red',
        fontSize: 16,
    },

})