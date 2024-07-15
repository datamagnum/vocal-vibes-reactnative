import { createStackNavigator } from "@react-navigation/stack";
import { NavigationContainer } from "@react-navigation/native";
import {
  createDrawerNavigator,
  DrawerContentScrollView,
  DrawerItemList,
  DrawerItem,
} from "@react-navigation/drawer";

import { Example, Startup, Login, Dashboard, Sessions } from "@/screens";
import { useTheme } from "@/theme";
import {
  View,
  ActivityIndicator,
  Text,
  TouchableOpacity,
  ScrollView,
  Alert,
} from "react-native";
import type {
  ApplicationDrawerScreenProps,
  ApplicationScreenProps,
  ApplicationStackParamList,
} from "@/types/navigation";
import SignUp from "@/screens/SignUp/SignUp";
import React, { useEffect, useState } from "react";
import StorageService from "@/services/storage.service";
import { StorageKeys } from "@/constants/storage.constant";
import { DrawerHeader } from "@/components/headers";
import SelfPractice from "@/screens/SelfPractice/SelfPractice";
import Groups from "@/screens/Group/Group";

const Stack = createStackNavigator<ApplicationStackParamList>();
const Drawer = createDrawerNavigator<ApplicationDrawerScreenProps>();

function ApplicationNavigator() {
  const [isLoginNavigator, setIsLoginNavigator] = useState<boolean>(true);
  const [isloggedIn, setIsLoggedIn] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      const token = await StorageService.getItem(StorageKeys.AUTH_TOKEN);
      console.log(token);
      setIsLoggedIn(token ? true : false);
    };
    fetchData();
  }, [isLoginNavigator]);

  if (!isloggedIn) {
    return (
      <NavigationContainer>
        <Stack.Navigator
          screenOptions={{ headerShown: false }}
          initialRouteName={"Login"}
        >
          <Stack.Screen name="Login">
            {(props: ApplicationScreenProps) => (
              <Login {...props} setIsLoginNavigator={setIsLoginNavigator} />
            )}
          </Stack.Screen>
          <Stack.Screen name="SignUp" component={SignUp} />
        </Stack.Navigator>
      </NavigationContainer>
    );
  }

  return (
    <NavigationContainer>
      <Drawer.Navigator
        drawerContent={(props) => (
          <DrawerContentScrollView {...props}>
            <DrawerHeader />
            <DrawerItemList {...props} />
            <DrawerItem
              label="Logout"
              onPress={async () => {
                console.log("here");
                await StorageService.removeItem(StorageKeys.AUTH_TOKEN);
                setIsLoginNavigator(true);
              }}
            />
          </DrawerContentScrollView>
        )}
        initialRouteName={"Dashboard"}
      >
        <Drawer.Screen name="Dashboard" component={Dashboard} />
        <Drawer.Screen name="Self Practice" component={SelfPractice} />
        <Drawer.Screen name="Sessions" component={Sessions} />
        <Drawer.Screen name="Groups" component={Groups} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}

export default ApplicationNavigator;
