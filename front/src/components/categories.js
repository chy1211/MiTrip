import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import React, {useState} from 'react';
import { styles } from '../screens/styles';
import { theme } from '../theme';
import { sortCategoryData } from '../constants';

export default function SortCategories({ activeCategory, setActiveCategory}) {
    // const [active, setActive] = React.useState('最新消息');
    
    return (
        <View style={styles.categoriesContainer2}>
            {sortCategoryData.map((sort, index) => {
                let isActive = activeCategory === sort;
                return (
                    <View key={sort} style={styles.buttonContainer}>
                            <TouchableOpacity
                                style={[styles.button, isActive && theme.activeButton]}
                                    onPress={() => setActiveCategory(sort)}>
                                <Text style={[styles.desttouch, isActive && theme.text]}>{sort}</Text>
                            </TouchableOpacity>
                    </View>
                );
            })}
        </View>
    );
}
