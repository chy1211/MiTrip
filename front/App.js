import React from "react";
import Tabs from "./src/navigation/tabs";
import { NavigationContainer } from "@react-navigation/native";
import MyDrawers from "./src/navigation/drawer";
import { createStackNavigator } from "@react-navigation/stack";
import { RotateInUpLeft } from "react-native-reanimated";
import HomeScreen from "./src/screens/HomeScreen";
import { StatusBar } from "expo-status-bar";
import AppNavigator from "./src/navigation";
import AuthNavigator from "./src/navigation/auth";
import { AuthProvider } from "./src/Context/AuthContext";
import AppNav from "./src/navigation/AppNav";
import { View } from "react-native";
import { CityDataProvider } from "./src/Context/CityDataContext";


const Stack = createStackNavigator()


// const App = ({showBottomTab}) => {
//   return (
    
//     // <NavigationContainer>
//     //   <StatusBar style="auto" />
//     //   {showBottomTab ? <Tabs /> : <MyDrawers />}
      
//     // </NavigationContainer>
//     <AuthNavigator />
//     //<AppNavigator />
//   );
// }
const App = () => {
  return (
    
    // <NavigationContainer>
    //   <StatusBar style="auto" />
    //   {showBottomTab ? <Tabs /> : <MyDrawers />}
      
    // </NavigationContainer>
    <AuthProvider>
        
        <AppNav />
    </AuthProvider>
    
    // <AppNavigator />
  
      // <Review/>

  );
}

// export default function App() {
//   return (
//     <AppNavigation />
//   );
// }
export default App;