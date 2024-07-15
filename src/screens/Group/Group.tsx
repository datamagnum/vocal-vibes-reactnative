import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import CreateGroupScreen from "@/screens/Group/CreateGroupScreen";
import ListGroupsScreen from "@/screens/Group/ListGroupScreen";
import { Text } from "react-native-paper";

const Tab = createBottomTabNavigator();

function Groups() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarOptions: {
          activeTintColor: "tomato",
          inactiveTintColor: "gray",
        },
        tabBarLabel: () => null,
        tabBarIcon: () => <Text>{route.name}</Text>, // No icon in addition to the label
      })}
    >
      <Tab.Screen
        name="Create"
        component={CreateGroupScreen}
        // options={{ title: "Create Group" }}
      />
      <Tab.Screen
        name="List"
        component={ListGroupsScreen}
        // options={{ title: "List Groups" }}
      />
    </Tab.Navigator>
  );
}

export default Groups;
