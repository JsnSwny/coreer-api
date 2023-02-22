import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import React from "react";
import { View, Pressable, StyleSheet, Image, Text, Button } from "react-native";
import colors from "../config/colors";
import { faStar } from "@fortawesome/free-solid-svg-icons";
import { faStar as farStar } from "@fortawesome/free-regular-svg-icons";
import FollowUser from "./FollowUser";
import capitalise from "../utils/capitalise";
import { faLocationPin } from "@fortawesome/free-solid-svg-icons";

const ProfileBox = ({ user, navigation }) => {
  const handlePress = () => {
    navigation.navigate("Messaging", { toUser: user });
  };
  return (
    <React.Fragment>
      <View style={styles.profileBox}>
        <Image
          style={styles.profileImage}
          source={{
            uri: user.profile_photo,
          }}
        />
        <View style={styles.follow}>
          <FollowUser user={user} />
        </View>

        <View style={styles.profileContent}>
          <Text style={styles.name}>
            {user.first_name} {user.last_name}
          </Text>
          {user.job && <Text>{capitalise(user.job)}</Text>}
          {user.location && (
            <View
              style={{
                flexDirection: "row",
                alignItems: "center",
                marginTop: 4,
              }}
            >
              <FontAwesomeIcon
                icon={faLocationPin}
                style={{ marginRight: 4 }}
                size={12}
                color={colors.black}
              />
              <Text style={{ fontSize: 12 }}>{user.location}</Text>
            </View>
          )}
          <Text style={styles.description}>{user.bio}</Text>
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
    marginTop: 56,
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
    marginTop: 12,
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
  follow: {
    position: "absolute",
    right: 16,
    top: 16,
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
