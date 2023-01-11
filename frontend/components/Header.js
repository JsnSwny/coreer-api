import React from "react";
import { StyleSheet, Text, StatusBar } from "react-native";
import colors from "../config/colors";

const Header = () => {
  return <Text style={styles.container}>coreer</Text>;
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.primary,
    color: "#fff",
    fontWeight: "bold",
    fontSize: 16,
    paddingTop: StatusBar.currentHeight + 16,
    paddingBottom: 16,
    paddingLeft: 24,
    paddingRight: 24,
  },
});

export default Header;
