import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableWithoutFeedback,
  TouchableOpacity,
} from "react-native";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import colors from "../config/colors";
import { useRoute } from "@react-navigation/native";

const NavigationItem = ({ icon, name, navigation }) => {
  const route = useRoute();
  const active = route.name == name;
  return (
    <TouchableOpacity
      style={styles.container}
      onPress={() => navigation.navigate(name)}
    >
      <View style={[styles.icon, active && styles.iconActive]}>
        <FontAwesomeIcon
          color={active ? colors.primary : colors.black}
          size={22}
          icon={icon}
        />
      </View>
      <Text style={[styles.text, active && styles.textActive]}>{name}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "33.33%",
    alignItems: "center",
  },
  icon: {
    backgroundColor: "#fff",
    width: 34,
    height: 34,
    borderRadius: 17,
    justifyContent: "center",
    alignItems: "center",
  },
  iconActive: {
    backgroundColor: colors.lightPrimary,
  },
  text: {
    fontSize: 10,
    marginTop: 2,
  },
  textActive: {
    fontWeight: "bold",
  },
});

export default NavigationItem;
