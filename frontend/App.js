import { StyleSheet, Text, View } from "react-native";
import Explore from "./screens/Explore";
import Profile from "./screens/Profile";
import Inbox from "./screens/Inbox";
import Account from "./screens/Account";
import LoginScreen from "./screens/LoginScreen";
import MessagingScreen from "./screens/MessagingScreen";
import colors from "./config/colors";
import { NavigationContainer, DefaultTheme } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Icon from "react-native-vector-icons/Ionicons";
import React from "react";
import * as SecureStore from "expo-secure-store";
import { AuthProvider } from "./context/AuthContext";
import { useAuth } from "./context/AuthContext";
import SignupScreen from "./screens/SignupScreen";
import OnboardingIntro from "./screens/onboarding/OnboardingIntro";
import OnboardingPersonalDetails from "./screens/onboarding/OnboardingPersonalDetails";
import SearchScreen from "./screens/SearchScreen";
import FavouritesScreen from "./screens/FavouritesScreen";

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
          } else if (route.name === "Favourites") {
            iconName = focused ? "star" : "star-outline";
          }

          // You can return any component that you like here!
          return (
            <View style={styles.tabItem}>
              <Icon name={iconName} size={size} color={color} />
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
      <Tab.Screen name="Favourites" component={FavouritesScreen} />
      <Tab.Screen name="Account" component={Account} />
    </Tab.Navigator>
  );
};

const OnboardingStack = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarStyle: { display: "none" },
      })}
    >
      {/* <Tab.Screen name="OnboardingIntro" component={OnboardingIntro} /> */}
      <Tab.Screen
        name="OnboardingPersonalDetails"
        component={OnboardingPersonalDetails}
      />
    </Tab.Navigator>
  );
};

const StackNavigation = () => {
  const { state, dispatch } = useAuth();
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      {state.userToken == null ? (
        <>
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Signup" component={SignupScreen} />
        </>
      ) : !state.user.onboarded ? (
        <>
          <Stack.Screen name="Onboarding" component={OnboardingStack} />
        </>
      ) : (
        <>
          <Stack.Screen name="Home" component={MyTabs} />
          <Stack.Screen name="Profile" component={Profile} />
          <Stack.Screen name="Messaging" component={MessagingScreen} />
          <Stack.Screen name="Search" component={SearchScreen} />
        </>
      )}
    </Stack.Navigator>
  );
};

const MyTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: "#FAFCFF",
  },
};

export default function App() {
  return (
    <NavigationContainer theme={MyTheme}>
      <AuthProvider>
        <StackNavigation />
      </AuthProvider>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
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
