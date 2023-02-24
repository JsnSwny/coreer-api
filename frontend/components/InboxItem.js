import React from "react";
import { View, Image, Text, StyleSheet, TouchableOpacity } from "react-native";
import colors from "../config/colors";

const InboxItem = ({ conversation, navigation }) => {
  const handlePress = () => {
    navigation.navigate("Messaging", { toUser: conversation.other_user });
  };
  return (
    <TouchableOpacity onPress={handlePress}>
      <View style={styles.container}>
        <Image
          style={styles.image}
          source={{
            uri: `${conversation.other_user.profile_photo}`,
          }}
        />
        <View>
          <Text style={styles.name}>{conversation.other_user.first_name}</Text>
          <Text style={styles.preview}>
            {conversation.last_message.content}
          </Text>
        </View>
      </View>
    </TouchableOpacity>
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
