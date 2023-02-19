import { StyleSheet } from "react-native";
import colors from "./colors";

export default StyleSheet.create({
  input: {
    backgroundColor: "#fff",
    height: 50,
    borderWidth: 0.5,
    borderRadius: 10,
    paddingHorizontal: 20,
    color: colors.grey,
    borderColor: colors.stroke,
    fontSize: 14,
  },
  shadowProp: {
    shadowOffset: { width: 5, height: 5 },
    shadowColor: "#96AAB4",
    shadowOpacity: 0.4,
    elevation: 5,
  },
});
