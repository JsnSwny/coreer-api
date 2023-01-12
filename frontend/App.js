import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import Explore from "./screens/Explore";
import Profile from "./screens/Profile";
import Inbox from "./screens/Inbox";
import Account from "./screens/Account";
import colors from "./config/colors";
import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Ionicons from "react-native-vector-icons/Ionicons";

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

const MyTabs = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarStyle: {},
        tabBarShowLabel: false,
        headerShown: false,
        tabBarHideOnKeyboard: true,

        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === "Explore") {
            iconName = focused ? "ios-home-sharp" : "ios-home-outline";
          } else if (route.name === "Inbox") {
            iconName = focused ? "chatbubble" : "chatbubble-outline";
          } else if (route.name === "Account") {
            iconName = focused ? "person" : "person-outline";
          }

          // You can return any component that you like here!
          return (
            <View style={styles.tabItem}>
              <Ionicons name={iconName} size={size} color={color} />
              <Text style={[styles.tabText, focused && styles.tabTextActive]}>
                {route.name}
              </Text>
            </View>
          );
        },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.grey,
      })}
    >
      <Tab.Screen name="Explore" component={Explore} />
      <Tab.Screen name="Inbox" component={Inbox} />
      <Tab.Screen name="Account" component={Account} />
    </Tab.Navigator>
  );
};

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Home" component={MyTabs} />
        <Stack.Screen name="Profile" component={Profile} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#FCFDFF",
    minHeight: "100%",
  },
  tabItem: {
    justifyContent: "center",
    alignItems: "center",
  },
  tabText: {
    fontSize: 10,
  },
  tabTextActive: {
    fontWeight: "bold",
    color: colors.primary,
  },
});
