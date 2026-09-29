import React, { useMemo,useState } from "react";
import {View, Text, ScrollView, SafeAreaView, StyleSheet, Button, Alert,TouchableOpacity } from 'react-native';
import RadioButtonGroup from 'react-native-radio-buttons-group';
import QuestionnairefetchData from "../components/QuestionnaireFetch";
import Icon from '@expo/vector-icons/Ionicons';
import { AuthContext } from "../Context/AuthContext";

const Questionnaire = ({navigation}) =>{
    const { userID } = React.useContext(AuthContext);
    // const [selectedAge, setSelectedAge] = useState();
    // const [selectedGender, setSelectedGender] = useState();
    // const [selectedJob, setSelectedJob] = useState();
    // const [selectedTravelDays, setSelectedTravelDays] = useState();
    // const [selectedTravelType, setSelectedTravelType] = useState();
    // const [selectedScheduleTime, setSelectedScheduleTime] = useState();
    // const [selectedTravelPeople, setSelectedTravelPeople] = useState();

    
    const questions = useMemo(
        () => [
        {
            id: 'Age',
            text: '1.您的年齡?',
            options: [
                { id: '0', label: '18歲以下', value: '18歲以下' },
                { id: '1', label: '18-24歲', value: '18-24歲' },
                { id: '2', label: '25-34歲', value: '25-34歲' },
                { id: '3', label: '35-44歲', value: '35-44歲' },
                { id: '4', label: '45-54歲', value: '45-54歲' },
                { id: '5', label: '55歲以上', value: '55歲以上' },
            ],
            // selectedValue: selectedAge,
            // setSelectedValue: setSelectedAge(selectedAge),
        },
        {
            id: 'Gender',
            text: '2.您的性別?',
            options: [
                { id: '0', label: '男', value: '男' },
                { id: '1', label: '女', value: '女' },
                { id: '2', label: '不願透漏', value: '不願透漏' },
                { id: '3', label: '其他', value: '其他' },
            ],
            // selectedValue: selectedGender,
            // setSelectedValue: setSelectedGender,
        },
        {
            id: 'Job',
            text: '3.您的職業?',
            options: [
                { id: '0', label: '學生', value: '學生' },
                { id: '1', label: '家管', value: '家管' },
                { id: '2', label: '工商業人員', value: '工商業人員' },
                { id: '3', label: '自由業', value: '自由業' },
                { id: '4', label: '軍公教人員', value: '軍公教人員' },
                { id: '5', label: '醫護人員', value: '醫護人員' },
                { id: '6', label: '其他', value: '其他' },
            ],
            // selectedValue: selectedJob,
            // setSelectedValue: setSelectedJob,
        },
        {
            id: 'TravelDays',
            text: '4.您通常會花幾天在國內旅行?',
            options: [
                { id: '0', label: '1天', value: '1天' },
                { id: '1', label: '2天', value: '2天' },
                { id: '2', label: '3~4天', value: '3~4天' },
                { id: '3', label: '5~6天', value: '5~6天' },
                { id: '4', label: '7天或以上', value: '7天或以上' },
            ],
            // selectedValue: selectedTravelDays,
            // setSelectedValue: setSelectedTravelDays,
        },
        {
            id: 'TravelDaysBudget1',
            text: '5.請問如果出遊1天您願意花費多少預算?',
            options: [
                { id: '0', label: '5,000元以下', value: '5,000元以下' },
                { id: '1', label: '5,000-10,000元', value: '5,000-10,000元' },
                { id: '2', label: '10,000-30,000元', value: '10,000-30,000元' },
                { id: '3', label: '30,000元以上', value: '30,000元以上' },
            ],
            // selectedValue: selectedTravelDays,
            // setSelectedValue: setSelectedTravelDays,
        },
        {
            id: 'TravelDaysBudget2',
            text: '6.請問如果出遊2天您願意花費多少預算?',
            options: [
                { id: '0', label: '5,000元以下', value: '5,000元以下' },
                { id: '1', label: '5,000-10,000元', value: '5,000-10,000元' },
                { id: '2', label: '10,000-30,000元', value: '10,000-30,000元' },
                { id: '3', label: '30,000元以上', value: '30,000元以上' },
            ],
            // selectedValue: selectedTravelDays,
            // setSelectedValue: setSelectedTravelDays,
        },
        {
            id: 'TravelDaysBudget3',
            text: '7.請問如果出遊3-4天您願意花費多少預算?',
            options: [
                { id: '0', label: '5,000元以下', value: '5,000元以下' },
                { id: '1', label: '5,000-10,000元', value: '5,000-10,000元' },
                { id: '2', label: '10,000-30,000元', value: '10,000-30,000元' },
                { id: '3', label: '30,000元以上', value: '30,000元以上' },
            ],
            // selectedValue: selectedTravelDays,
            // setSelectedValue: setSelectedTravelDays,
        },
        {
            id: 'TravelDaysBudget5',
            text: '8.請問如果出遊5-6天您願意花費多少預算?',
            options: [
                { id: '0', label: '10,000元以下', value: '10,000元以下' },
                { id: '1', label: '10,000-30,000元', value: '10,000-30,000元' },
                { id: '2', label: '30,000-50,000元', value: '10,000-50,000元' },
                { id: '3', label: '50,000元以上', value: '50,000元以上' },
            ],
            // selectedValue: selectedTravelDays,
            // setSelectedValue: setSelectedTravelDays,
        },
        {
            id: 'TravelDaysBudget7',
            text: '9.請問如果出遊7天或以上您願意花費多少預算? ',
            options: [
                { id: '0', label: '10,000元以下', value: '10,000元以下' },
                { id: '1', label: '10,000-30,000元', value: '10,000-30,000元' },
                { id: '2', label: '30,000-50,000元', value: '10,000-50,000元' },
                { id: '3', label: '50,000元以上', value: '50,000元以上' },
            ],
            // selectedValue: selectedTravelDays,
            // setSelectedValue: setSelectedTravelDays,
        },
        {
            id: 'TravelType',
            text: '10.您喜歡什麼樣的旅遊方式?',
            options: [
                { id: '0', label: '自助旅行', value: '自助旅行' },
                { id: '1', label: '跟團旅行', value: '跟團旅行' },
                { id: '2', label: '都喜歡', value: '都喜歡' },
                { id: '3', label: '其他旅遊方式', value: '其他旅遊方式' },
            ],
            // selectedValue: selectedTravelType,
            // setSelectedValue: setSelectedTravelType,
        },
        {
            id: 'TravelSchedule',
            text: '11.您通常會在何時進行旅遊的規劃呢?',
            options: [
                { id: '0', label: '一周前或更短時間', value: '一周前或更短時間' },
                { id: '1', label: '一周~一個月前', value: '一周~一個月前' },
                { id: '2', label: '一個月~三個月前', value: '一個月~三個月前' },
                { id: '3', label: '三個月~六個月前', value: '三個月~六個月前' },
            ],
            // selectedValue: selectedScheduleTime,
            // setSelectedValue: setSelectedScheduleTime,
        },
        {
            id: 'TravelPeople',
            text: '12.通常會與多少人一起旅遊呢?',
            options: [
                { id: '0', label: '1個人', value: '1個人' },
                { id: '1', label: '2個人', value: '2個人' },
                { id: '2', label: '3~5個人', value: '3~5個人' },
                { id: '3', label: '6人以上', value: '6人以上' },
            ],
            // selectedValue: selectedTravelPeople,
            // setSelectedValue: setSelectedTravelPeople,
        },
        {
            id: 'MtTravelType',
            text: '13.假如您要前往阿里山時，您偏好哪種交通方式呢?',
            options: [
                { id: '0', label: '大眾運輸', value: '大眾運輸1' },
                { id: '1', label: '自駕', value: '自駕1' },
            ],
            // selectedValue: selectedScheduleTime,
            // setSelectedValue: setSelectedScheduleTime,
        },
        {
            id: 'CityTravelDays',
            text: '14.假如您要前往市中心時，您偏好哪種交通方式呢?',
            options: [
                { id: '0', label: '大眾運輸', value: '大眾運輸2' },
                { id: '1', label: '自駕', value: '自駕2' },
            ],
            // selectedValue: selectedScheduleTime,
            // setSelectedValue: setSelectedScheduleTime,
        },
        {
            id: 'PurchasedItem',
            text: '15.請問您過去旅遊時曾購買那些種類的商品呢?',
            options: [
                { id: '0', label: '不太購買商品', value: '不太購買商品' },
                { id: '1', label: '奢侈品等高檔商品', value: '奢侈品等高檔商品' },
                { id: '2', label: '當地土產、特產', value: '當地土產、特產' },
                { id: '3', label: '當地手工藝品、文化用品等特色商品', value: '當地手工藝品、文化用品等特色商品' },
            ],
            // selectedValue: selectedScheduleTime,
            // setSelectedValue: setSelectedScheduleTime,
        },
        {
            id: 'TravelInfo',
            text: '16.請問您通常會使用那些渠道獲取旅遊資訊呢?',
            options: [
                { id: '0', label: '旅遊公司官方網站或實體店面', value: '旅遊公司官方網站或實體店面' },
                { id: '1', label: '旅遊書籍或雜誌', value: '旅遊書籍或雜誌' },
                { id: '2', label: '旅遊相關網站或APP', value: '旅遊相關網站或APP' },
                { id: '3', label: '朋友親戚或同事推薦', value: '朋友親戚或同事推薦' },
                { id: '4', label: '網路搜尋引擎', value: '網路搜尋引擎' },
            ],
            // selectedValue: selectedScheduleTime,
            // setSelectedValue: setSelectedScheduleTime,
        },
        {
            id: 'TravelNeeds',
            text: '17.請問您覺得在旅遊中能夠滿足那些需求?',
            options: [
                { id: '0', label: '不用看到討厭的人', value: '不用看到討厭的人' },
                { id: '1', label: '增長見聞、學習新技能', value: '增長見聞、學習新技能' },
                { id: '2', label: '放鬆身心、紓解壓力', value: '放鬆身心、紓解壓力' },
                { id: '3', label: '獨立探險、尋找新鮮感', value: '獨立探險、尋找新鮮感' },
                { id: '4', label: '與親友共遊、增進感情', value: '與親友共遊、增進感情' },
                { id: '5', label: '體驗當地文化、風俗習慣', value: '體驗當地文化、風俗習慣' },
            ],
            // selectedValue: selectedScheduleTime,
            // setSelectedValue: setSelectedScheduleTime,
        },
        {
            id: 'TravelMedia',
            text: '18.當您要出遊時會使用什麼方式去安排行程呢?',
            options: [
                { id: '0', label: 'Google Maps', value: 'Google Maps' },
                { id: '1', label: 'Vlog/部落格', value: 'Vlog/部落格' },
                { id: '2', label: '旅遊網站/APP', value: '旅遊網站/APP' },
                { id: '3', label: '其他方式', value: '其他方式' },
            ],
            // selectedValue: selectedScheduleTime,
            // setSelectedValue: setSelectedScheduleTime,
        },
        
        ],
        []
    );

    const [selectedValues, setSelectedValues] = useState({});

    const renderQuestion = (question) => {
    return (
        <View key={question.id} style={styles.QuestionContainer}>
            <Text style={{ fontSize: 24, marginBottom:10 }}>{question.text}</Text>
            <RadioButtonGroup
                containerStyle={{ alignSelf: 'flex-start', alignItems: 'flex-start', maxWidth: 300 }}
                radioButtons={question.options}
                onPress={(selectedButton) => {
                console.log(`Selected ${question.id}:`, selectedButton);
                console.log(`Saving ${question.id}:`, selectedValues);
                setSelectedValues((prevValues) => ({
                ...prevValues,
                [question.id]: selectedButton,
            }));
            }}
            selectedId={selectedValues[question.id]}
        />
        </View>
    );
    };

    const onSubmit = async() =>{
        console.log('onsubmit',selectedValues);
        console.log('onsubmit',userID);

        // 檢查是否有遺漏的題目
        const unansweredQuestions = questions.filter(question => !selectedValues[question.id]);
        if (unansweredQuestions.length > 0) {
            // 顯示警告，提示使用者回答遺漏的題目
            const unansweredQuestionTexts = unansweredQuestions.map(question => question.text);
            Alert.alert('警告', `請回答以下遺漏的題目：\n${unansweredQuestionTexts.join('\n')}`);
            return;
        }
        if (!userID) {
            Alert.alert('提示', '請先登入再填寫問卷');
            return;
        }
        const response = await QuestionnairefetchData(
            selectedValues['Age'],
            selectedValues['Gender'],
            selectedValues['Job'],
            selectedValues['TravelDays'],
            selectedValues['TravelDaysBudget1'],
            selectedValues['TravelDaysBudget2'],
            selectedValues['TravelDaysBudget3'],
            selectedValues['TravelDaysBudget5'],
            selectedValues['TravelDaysBudget7'],
            selectedValues['TravelType'],
            selectedValues['TravelSchedule'],
            selectedValues['TravelPeople'],
            selectedValues['MtTravelType'],
            selectedValues['CityTravelDays'],
            selectedValues['PurchasedItem'],
            selectedValues['TravelInfo'],
            selectedValues['TravelNeeds'],
            selectedValues['TravelMedia'],
            userID,
        );

        // 檢查是否成功
        if (response.success) {
            // 送出後回到上一頁（2023 版停留在問卷頁，可以再按一次重複送出）
            Alert.alert('Success', '您的問卷已經成功送出', [{ text: 'OK', onPress: () => navigation.goBack() }]);
        } else {
            // 如果有錯誤，顯示警告；已填過就回上一頁，其他錯誤留在原頁以免答案遺失
            const alreadyFilled = response.error === '您已經填寫過問卷';
            Alert.alert('Error', response.error, alreadyFilled ? [{ text: 'OK', onPress: () => navigation.goBack() }] : undefined);
        }
    };
    
    return(
        <SafeAreaView style={{flex:1, backgroundColor:'white',width:'100%',justifyContent:'start',alignSelf:'center',alignItems:'center',marginTop:25,}}>
            <TouchableOpacity 
                style={{position:'absolute', left:10,top:50,zIndex:10,}}
                onPress={() => navigation.goBack()}
                >
                <View style={{flexDirection:'row',alignItems:'center'}}>
                    <Icon name="arrow-undo" size={30} color={'gray'}/>
                    <Text style={{marginLeft:3}}>返回</Text>
                </View>
            </TouchableOpacity>
            <ScrollView style={{flex:1, width:'80%'}}>
                <Text style={{fontSize:50,fontWeight:'bold',alignSelf:'center',top:50}}>行程偏好問卷</Text>
                {questions.map(renderQuestion)}
                <View style={{backgroundColor:'white', width:250,borderRadius:10,marginTop:15,alignSelf:'center', marginBottom:20}}>
                    <Button mode="contained-tonal" title='繳交'  onPress={() => onSubmit()}></Button>
                </View>
            </ScrollView>
        </SafeAreaView>
    )

}

const styles = StyleSheet.create({
    QuestionContainer:{
        width:"80%",
        alignSelf:'center',
        alignItems:'flex-start',
        padding:10,
        paddingHorizontal:20,
        marginTop:100,
        backgroundColor:'white',
        borderRadius:20,
        borderWidth:2,
        shadowColor:'#000',
        shadowOffset: { width: 10, height: 15 }, // 陰影的偏移量，右下角
        shadowOpacity: 0.5, // 陰影的透明度
        shadowRadius: 6, // 陰影的模糊半徑
        elevation: 5, // Android 上陰影的高度
},
})

export default Questionnaire



{/* <View style={styles.QuestionContainer}>
                    <Text style={{fontSize:30}}>1.您的年齡?</Text> */}
                    {/* <RadioButtonGroup 
                        containerStyle={{alignSelf:'flex-start',alignItems:'flex-start',maxWidth:90}}
                        radioButtons={QuestionAge}
                        onPress={(selectedButton) => {
                            const selectedAge = selectedButton;
                            console.log('return',selectedAge);
                            setSelectedAge(selectedAge);
                        }}
                        selectedId={selectedAge}
                        /> */}
                        {/* {renderRadioButtonGroup(QuestionAge, selectedAge, setSelectedAge)} */}
                {/* </View>
                <View style={styles.QuestionContainer}>
                    <Text style={{fontSize:30}}>2.您的性別?</Text> */}
                    {/* <RadioButtonGroup 
                        containerStyle={{alignSelf:'flex-start',alignItems:'flex-start',maxWidth:90}}
                        radioButtons={QuestionAge}
                        onPress={(selectedButton) => {
                            const selectedAge = selectedButton;
                            console.log('return',selectedAge);
                            setSelectedAge(selectedAge);
                        }}
                        selectedId={selectedAge}
                        /> */}
                        {/* {renderRadioButtonGroup(QuestionAge, selectedAge, setSelectedAge)} */}
                {/* </View> */}

                //問題1年齡
    // const QuestionAge = useMemo(() => ([
    //     {
    //         id: '0', // acts as primary key, should be unique and non-empty string
    //         label: '18歲以下',
    //         value: '18歲以下'
    //     },
    //     {
    //         id: '1',
    //         label: '18-24歲',
    //         value: '18-24歲'
    //     },
    //     {
    //         id: '2',
    //         label: '25-34歲',
    //         value: '25-34歲'
    //     },
    //     {
    //         id: '3',
    //         label: '35-44歲',
    //         value: '35-44歲'
    //     },
    //     {
    //         id: '4',
    //         label: '45-54歲',
    //         value: '45-54歲'
    //     },
    //     {
    //         id: '5',
    //         label: '55歲以上',
    //         value: '55歲以上'
    //     }
        
    // ]), []);
    // const QuestionSex = useMemo(() => ([
    //     {
    //         id: '0', // acts as primary key, should be unique and non-empty string
    //         label: '男',
    //         value: '男'
    //     },
    //     {
    //         id: '1',
    //         label: '女',
    //         value: '女'
    //     },
    //     {
    //         id: '2',
    //         label: '不願透漏',
    //         value: '不願透漏'
    //     },
    //     {
    //         id: '3',
    //         label: '其他',
    //         value: '其他'
    //     },
        
    // ]), []);