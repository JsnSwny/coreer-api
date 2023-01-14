import React from "react";
import { View, Pressable, StyleSheet, Image, Text, Button } from "react-native";
import colors from "../config/colors";

const ProfileBox = ({ user, navigation }) => {
  const handlePress = () => {
    navigation.navigate("Messaging", { user });
  };
  return (
    <React.Fragment>
      <View style={styles.profileBox}>
        <Image
          style={styles.profileImage}
          source={{
            uri: user.image,
          }}
        />
        <View style={styles.tag}>
          <Text style={styles.tagText}>72% Match</Text>
        </View>
        <View style={styles.profileContent}>
          <Text style={styles.name}>
            {user.first_name} {user.last_name}
          </Text>
          <Text style={styles.description}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Montes,
            venenatis, sit suspendisse ullamcorper lectus dui, dictumst quis.
            Senectus donec duis nec sed morbi.
          </Text>
          <Pressable style={styles.button} onPress={handlePress}>
            <Text style={styles.buttonText}>Message {user.name}</Text>
          </Pressable>
        </View>
      </View>
    </React.Fragment>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 16,
  },
  headerCircle: {
    width: "150%",
    height: 200,
    backgroundColor: colors.primary,
    position: "absolute",
    zIndex: -1,
  },
  profileBox: {
    width: "100%",
    marginTop: 48,
    backgroundColor: "#fff",
    borderRadius: 10,
    borderWidth: 1,
    borderColor: colors.stroke,
    padding: 16,
  },
  profileImage: {
    width: 100,
    height: 100,
    position: "absolute",
    top: -40,
    left: 12,
    borderRadius: 50,
    borderWidth: 4,
    borderColor: "#fff",
  },
  profileContent: {
    marginTop: 50,
  },
  name: {
    fontWeight: "bold",
    fontSize: 20,
    color: colors.black,
  },
  description: {
    color: colors.grey,
    marginTop: 4,
    marginBottom: 24,
    fontSize: 14,
    lineHeight: 20,
  },
  button: {
    backgroundColor: colors.primary,
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 10,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
  tag: {
    position: "absolute",
    right: 16,
    top: 16,
    backgroundColor: colors.lightGreen,
    borderRadius: 5,
  },
  tagText: {
    fontSize: 12,
    color: colors.green,
    paddingVertical: 4,
    paddingHorizontal: 10,
    fontWeight: "bold",
  },
});

export default ProfileBox;
