import React from "react";
import {
  StyleSheet,
  View,
  Text,
  StatusBar,
  TouchableWithoutFeedback,
} from "react-native";
import colors from "../config/colors";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";

const Header = ({ title, backButton, navigation, color = true }) => {
  return (
    <TouchableWithoutFeedback onPress={() => backButton && navigation.goBack()}>
      <View style={[styles.container, color && styles.containerColor]}>
        {backButton && (
          <FontAwesomeIcon
            icon={faArrowLeft}
            style={[styles.title, styles.back]}
          />
        )}
        <Text style={styles.title}>{title}</Text>
      </View>
    </TouchableWithoutFeedback>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingTop: StatusBar.currentHeight + 16,
    paddingBottom: 16,
    paddingHorizontal: 16,
    flexDirection: "row",
    alignItems: "center",
  },
  containerColor: {
    backgroundColor: colors.primary,
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
