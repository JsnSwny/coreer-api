import React from "react";
import { Text, StyleSheet, View } from "react-native";
import colors from "../config/colors";
import NavigationItem from "./NavigationItem";
import { faHouse } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-solid-svg-icons";
import { faUser } from "@fortawesome/free-solid-svg-icons";

const Navigation = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <NavigationItem navigation={navigation} icon={faHouse} name="Explore" />
      <NavigationItem navigation={navigation} icon={faComment} name="Inbox" />
      <NavigationItem navigation={navigation} icon={faUser} name="Account" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: "#fff",
    position: "absolute",
    bottom: 0,
    borderTopRightRadius: 25,
    borderTopLeftRadius: 25,
    borderWidth: 1,
    borderColor: colors.stroke,
    flexDirection: "row",
    alignItems: "center",
    zIndex: 10,
  },
});

export default Navigation;
