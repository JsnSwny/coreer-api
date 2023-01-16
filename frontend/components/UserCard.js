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
import Icon from "react-native-vector-icons/FontAwesome";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { faLocationDot } from "@fortawesome/free-solid-svg-icons/faLocationDot";
import { faStar } from "@fortawesome/free-solid-svg-icons";
import { useAuth, useAuthState, useAuthDispatch } from "../context/AuthContext";
import axios from "axios";
import { API_URL } from "@env";

const UserCard = ({ user, navigation }) => {
  const authState = useAuthState();
  const authDispatch = useAuthDispatch();

  const likeUser = () => {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    config.headers["Authorization"] = `Token ${authState.userToken}`;
    let newLikes = authState.user.likes;

    if (authState.user.likes.includes(user.id)) {
      newLikes = [...newLikes.filter((item) => item != user.id)];
    } else {
      newLikes.push(user.id);
    }

    axios
      .put(
        `${API_URL}/api/profiles/${authState.user.id}/`,
        {
          likes: newLikes,
        },
        config
      )
      .then((res) => {
        authDispatch({
          type: "UPDATE_LIKES",
          likes: res.data.likes,
        });
      })

      .catch((err) => console.log("error"));
  };

  const handlePress = () => {
    navigation.navigate("Profile", { user });
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
            <Text style={styles.name}>
              {user.first_name} {user.last_name}
            </Text>
            <Text style={styles.role}>{user.currentRole}</Text>
            <View style={{ flexDirection: "row", marginTop: 8 }}>
              <FontAwesomeIcon color={colors.grey} icon={faLocationDot} />
              <Text style={styles.location}>{user.location}</Text>
            </View>
          </View>
        </View>
        <View style={styles.horizontalLine} />
        <View style={styles.cardBottom}>
          <Text style={styles.tag}>Professional</Text>
          <TouchableOpacity onPress={likeUser}>
            <FontAwesomeIcon
              color={
                authState.user.likes.includes(user.id)
                  ? colors.primary
                  : colors.black
              }
              icon={faStar}
              size={20}
            />
          </TouchableOpacity>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  name: { fontSize: 16, fontWeight: "bold" },
  role: { fontSize: 14, color: colors.grey },
  location: {
    fontSize: 12,
    color: colors.grey,
    marginLeft: 4,
  },
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
    backgroundColor: colors.lightPrimary,
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
