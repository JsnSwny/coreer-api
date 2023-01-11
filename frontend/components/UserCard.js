import React from "react";
import {
  Text,
  Image,
  View,
  StyleSheet,
  TouchableHighlight,
  TouchableOpacity,
} from "react-native";
import colors from "../config/colors";

const UserCard = ({ user, navigation }) => {
  const handlePress = () => {
    navigation.navigate("Profile");
  };
  return (
    <TouchableOpacity
      activeOpacity={0.5}
      style={{ marginBottom: 16 }}
      onPress={handlePress}
    >
      <View style={styles.card}>
        <View style={styles.cardTop}>
          <Image
            style={styles.profile}
            source={{
              uri: user.image,
            }}
          />
          <View>
            <Text style={styles.name}>{user.name}</Text>
            <Text style={styles.role}>{user.currentRole}</Text>
            <Text style={styles.location}>{user.location}</Text>
          </View>
        </View>
        <View style={styles.horizontalLine} />
        <View style={styles.cardBottom}>
          <Text style={styles.tag}>Professional</Text>
          <Image style={styles.icon} source={require("../assets/heart.png")} />
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  name: { fontSize: 16, fontWeight: "bold" },
  role: { fontSize: 14, color: colors.grey },
  location: { fontSize: 12, color: colors.grey },
  profile: { width: 70, height: 70, marginRight: 16, borderRadius: 35 },
  card: {
    borderRadius: 10,
    borderColor: colors.stroke,
    borderWidth: 1,
    backgroundColor: "#fff",
    padding: 16,
    flex: 0,
    height: "auto",
  },
  cardTop: {
    flexDirection: "row",
    alignItems: "center",
  },
  horizontalLine: {
    borderBottomColor: colors.stroke,
    borderBottomWidth: 1,
    marginVertical: 12,
  },
  cardBottom: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  tag: {
    color: colors.primary,
    backgroundColor: "rgba(25, 149, 185, 0.1)",
    padding: 8,
    borderRadius: 10,
    fontSize: 10,
    alignSelf: "flex-start",
  },
  icon: {
    width: 20,
    height: 20,
  },
});

export default UserCard;
