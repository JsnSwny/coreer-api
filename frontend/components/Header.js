import React from "react";
import {
  StyleSheet,
  View,
  Text,
  StatusBar,
  TouchableWithoutFeedback,
} from "react-native";
import colors from "../config/colors";

const Header = ({ title, backButton, navigation }) => {
  return (
    <TouchableWithoutFeedback onPress={() => backButton && navigation.goBack()}>
      <View style={styles.container}>
        {backButton && <Text style={[styles.title, styles.back]}>{"<"}</Text>}
        <Text style={styles.title}>{title}</Text>
      </View>
    </TouchableWithoutFeedback>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.primary,
    paddingTop: StatusBar.currentHeight + 16,
    paddingBottom: 16,
    paddingHorizontal: 16,
    flexDirection: "row",
    alignItems: "center",
  },
  title: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 16,
  },
  back: {
    marginRight: 8,
  },
});

export default Header;
