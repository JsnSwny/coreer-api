import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import Explore from "./screens/Explore";
import Profile from "./screens/Profile";
import colors from "./config/colors";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export default function App() {
  const Stack = createNativeStackNavigator();
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Explore" component={Explore} />
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
});
