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
import { faHome } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-solid-svg-icons";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { faStar } from "@fortawesome/free-solid-svg-icons";

// import { faHouseUser as farHome } from "@fortawesome/free-regular-svg-icons";
// import { faComment as farComment } from "@fortawesome/free-regular-svg-icons";
// import { faUser as farUser } from "@fortawesome/free-regular-svg-icons";
// import { faStar as farStar } from "@fortawesome/free-regular-svg-icons";

import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

const MyTabs = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarStyle: {
          height: 60,
          borderTopColor: colors.stroke,
          borderTopWidth: 0.5,
        },
        tabBarShowLabel: false,
        headerShown: false,
        tabBarHideOnKeyboard: true,

        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === "Explore") {
            iconName = focused ? faHome : faHome;
          } else if (route.name === "Inbox") {
            iconName = focused ? faComment : faComment;
          } else if (route.name === "Account") {
            iconName = focused ? faUser : faUser;
          } else if (route.name === "Favourites") {
            iconName = focused ? faStar : faStar;
          }

          // You can return any component that you like here!
          return (
            <View style={styles.tabItem}>
              <FontAwesomeIcon icon={iconName} size={size} color={color} />
              <Text style={[styles.tabText, focused && styles.tabTextActive]}>
                {route.name}
              </Text>
            </View>
          );
        },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.black,
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
      <LandingPage />
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
    marginTop: 4,
  },
  tabTextActive: {
    fontWeight: "bold",
    color: colors.primary,
  },
});
