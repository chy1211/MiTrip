import React, {useState} from 'react';
import { SafeAreaView, ScrollView, View, Text, TouchableOpacity, Image } from 'react-native';
import { styles } from './styles'; // 引入你的 styles.js
import Categories from '../components/categories';
import Categories2 from '../components/categories2';
import Destinations from '../components/dest';
import Destinations2 from '../components/dest2';
import Social from '../components/social';

export default function HomeScreen() {
    const [activeCategory, setActiveCategory] = useState('最新消息');

    return (
        <SafeAreaView style={[styles.safeAreaView, { backgroundColor: '#000' }]} >
            <ScrollView showsVerticalScrollIndicator={false} style={styles.scrollView}>
                <View style={{marginTop: 20}}>
                    {/* 通過傳遞回調函數给 SortCategories 组件 */}
                    <Categories activeCategory={activeCategory} setActiveCategory={setActiveCategory}/>

                    {/* 根據選中的分類來顯示不同的内容 */}
                    {activeCategory === '最新消息' && (
                        <View>
                            <Destinations />
                        </View>
                    )}
                    {activeCategory === '熱門商家' && (
                        <View>
                            <Destinations2 />
                        </View>
                    )}
                </View>

                {/* categories3 */}
                <View>
                    <Categories2 />
                </View>

                <View>
                    <Social />
                </View>

                
            </ScrollView>
        </SafeAreaView>
    );
}