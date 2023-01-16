import React from "react";
import { View, Image, Text, StyleSheet } from "react-native";
import colors from "../config/colors";

const InboxItem = () => {
  return (
    <View style={styles.container}>
      <Image
        style={styles.image}
        source={{
          uri: "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
        }}
      />
      <View>
        <Text style={styles.name}>Jason Sweeney</Text>
        <Text style={styles.preview}>Justo, proin ornare urna habitant...</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    borderBottomColor: colors.stroke,
    borderBottomWidth: 1,
    paddingBottom: 16,
    marginBottom: 16,
  },
  image: { width: 70, height: 70, marginRight: 16, borderRadius: 35 },
  name: {
    fontWeight: "bold",
    fontSize: 16,
    color: colors.black,
  },
  preview: {
    color: colors.grey,
  },
});

export default InboxItem;
