import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import Explore from "./screens/Explore";
import colors from "./config/colors";

export default function App() {
  return (
    <View style={styles.container}>
      <Explore />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#FCFDFF",
    minHeight: "100%",
  },
});
