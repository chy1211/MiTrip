import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import React, {useState} from 'react';
import { styles } from '../screens/styles';
import { theme } from '../theme';
import { lswitch } from '../constants';

export default function Ltineraryswitch({ activeCategory, setActiveCategory}) {
    // const [active, setActive] = React.useState('我的旅程');
    
    return (
        <View style={styles.categoriesContainer2}>
            {lswitch.map((sort, index) => {
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
