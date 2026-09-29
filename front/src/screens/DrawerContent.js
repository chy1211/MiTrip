import React, {useContext} from 'react';
import { View, StyleSheet, TouchableOpacity} from 'react-native';
import {
    useTheme,
    Avatar,
    Title,
    Caption,
    Paragraph,
    Drawer,
    Text,
    TouchableRipple,
    Switch
} from 'react-native-paper';
import {
    DrawerContentScrollView,
    DrawerItem,
    DrawerItemList
} from '@react-navigation/drawer';
import HomeScreen from './HomeScreen';
import { Image } from 'react-native';
import { MaterialIcons as Iconm, AntDesign as Icona, FontAwesome as Iconf, Ionicons as Icon } from '@expo/vector-icons';
import { AuthContext } from '../Context/AuthContext';
import AuthStack from '../navigation/auth';

export function DrawerContent(props) {
  const {logout} = useContext(AuthContext);
  const {username} = useContext(AuthContext);
  const {userToken} = useContext(AuthContext);

    return(
        <View style={{flex:1}}>
            <DrawerContentScrollView {... props}>
                <View style={styles.drawerContent}>
                {userToken === null ? (
                  <View style={{flexDirection:"row",paddingLeft:10,}}>
                    <Image source={require('../../assets/images/avatar.png')}
                            style={{height:80, width:80, borderRadius:40, marginBottom:10}} />
                      <Text style={{fontSize:22, marginLeft:20, marginTop:30}}>未登入</Text>
                  </View>
                    ) : (
                      <View style={{flexDirection:"row",paddingLeft:10,}}>
                      <Image source={require('../../assets/images/user_avatar.png')}
                              style={{height:80, width:80, borderRadius:40, marginBottom:10}} />
                      <Text style={{fontSize:24, marginLeft:20, marginTop:30}}>{username}</Text>
                    </View>
                    )}
                    <DrawerItem 
                              icon={({color, size}) => (
                                  <Iconm 
                                  name="explore" 
                                  color={color}
                                  size={size}
                                  />
                              )}
                              label="探索"
                              onPress={() => {props.navigation.navigate('tabs', { screen: '探索' })}}
                          />
                          
                      <DrawerItem 
                          icon={({color, size}) => (
                            <Iconf name='search'
                            size={size}
                            color={color}
                            />
                          )}
                          label='推薦'
                          onPress={() => {props.navigation.navigate('tabs', { screen: '推薦' })}}
                                  />
                      <DrawerItem 
                          icon={({color, size}) => (
                            <Icona name='calendar'
                            color={color}
                            size={size}
                            />
                          )}
                          label="行程"
                          onPress={() => {props.navigation.navigate('tabs', { screen: '行程' })}}
                      />
                      <DrawerItem
                                icon={({color, size}) => (
                                  <Icon 
                                  name="person-outline" 
                                  color={color}
                                  size={size}
                                  />
                              )} 
                          label="個人資訊"
                          onPress={() => {props.navigation.navigate('tabs', { screen: '個人' })}}
                      />
                      
                      
                      
                      
                </View>
                
            </DrawerContentScrollView>
            <Drawer.Section> 
              {userToken === null ?
              (<DrawerItem
                  icon={({color, size}) => (
                    <Icon 
                      name="exit-outline" 
                      color={color}
                      size={size}
                    />
                  )} 
                  label="登入"
                  onPress={() => props.navigation.navigate('Login')}
              />)
              :(
                <DrawerItem
                  icon={({color, size}) => (
                    <Iconm
                      name="login" 
                      color={color}
                      size={size}
                    />
                  )} 
                  label={"登出"}
                  onPress={() => {logout()}}
      />
              )
            }
        
              </Drawer.Section>
        </View>
    )
    



}



const styles = StyleSheet.create({
    drawerContent: {
      flex: 1,
    },
    userInfoSection: {
      paddingLeft: 20,
    },
    title: {
      fontSize: 16,
      marginTop: 3,
      fontWeight: 'bold',
    },
    caption: {
      fontSize: 14,
      lineHeight: 14,
    },
    row: {
      marginTop: 20,
      flexDirection: 'row',
      alignItems: 'center',
    },
    section: {
      flexDirection: 'row',
      alignItems: 'center',
      marginRight: 15,
    },
    paragraph: {
      fontWeight: 'bold',
      marginRight: 3,
    },
    drawerSection: {
      marginTop: 15,
    },
    bottomDrawerSection: {
        marginBottom: 15,
        borderTopColor: '#f4f4f4',
        borderTopWidth: 1
    },
    preference: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      paddingVertical: 12,
      paddingHorizontal: 16,
    },
  });