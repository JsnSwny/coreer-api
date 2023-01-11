import React from "react";
import { View, Text, StyleSheet } from "react-native";
import colors from "../config/colors";

const Title = ({ title, subtitle }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.subtitle}>{subtitle}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingLeft: 24,
    paddingRight: 24,
    paddingTop: 16,
    paddingBottom: 16,
  },
  title: {
    fontWeight: "bold",
    fontSize: 18,
    color: colors.black,
  },
  subtitle: {
    fontSize: 14,
    color: colors.grey,
    marginTop: 4,
    width: "70%",
  },
});

export default Title;
