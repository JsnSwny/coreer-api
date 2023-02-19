import React from "react";
import { View } from "react-native";

const Container = ({ children }) => (
  <View style={{ paddingHorizontal: 16 }}>{children}</View>
);

export default Container;
