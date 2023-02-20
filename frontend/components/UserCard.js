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
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import { API_URL } from "@env";
import globalStyles from "../config/globalStyles";

const UserCard = ({ user, navigation }) => {
  const { state, dispatch } = useAuth();

  const likeUser = () => {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    config.headers["Authorization"] = `Token ${state.userToken}`;
    let newLikes = state.user.following;

    if (state.user.following.includes(user.id)) {
      newLikes = [...newLikes.filter((item) => item != user.id)];
    } else {
      newLikes.push(user.id);
    }

    axios
      .post(
        `${API_URL}/api/follow/`,
        {
          follower: state.user.id,
          following: user.id,
        },
        config
      )
      .then((res) => {
        dispatch({
          type: "UPDATE_LIKES",
          likes: res.data.following,
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
      <View style={[styles.card, globalStyles.shadowProp]}>
        <View style={styles.cardTop}>
          <Image
            style={styles.profile}
            source={{
              uri: user.profile_photo,
            }}
          />
          <View style={{ flex: 1 }}>
            <Text style={styles.name}>
              {user.first_name} {user.last_name}
            </Text>
            <Text style={styles.role}>{user.job}</Text>
            <View
              style={{
                flexDirection: "row",
                marginTop: 8,
                flex: 1,
              }}
            >
              <FontAwesomeIcon color={colors.grey} icon={faLocationDot} />
              <Text style={styles.location}>{user.location}</Text>
            </View>
          </View>
        </View>
        <Text style={styles.bio}>{user.bio}</Text>
        <View style={styles.horizontalLine} />
        <View style={styles.cardBottom}>
          <Text style={styles.tag}>Professional</Text>
          <TouchableOpacity onPress={likeUser}>
            <FontAwesomeIcon
              color={
                state.user.following.includes(user.id)
                  ? colors.primary
                  : colors.black
              }
              icon={faStar}
              size={24}
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
    flex: 1,
  },
  bio: {
    marginTop: 12,
    color: colors.grey,
  },
  profile: { width: 70, height: 70, marginRight: 16, borderRadius: 35 },
  card: {
    borderRadius: 10,
    borderColor: colors.stroke,
    borderWidth: 0.5,
    backgroundColor: "#fff",
    padding: 16,
    flex: 0,
    height: "auto",
  },
  cardTop: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
  },

  horizontalLine: {
    borderBottomColor: colors.stroke,
    borderBottomWidth: 0.5,
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
