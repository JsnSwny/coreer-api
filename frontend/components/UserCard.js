import React from "react";
import {
  Text,
  Image,
  View,
  StyleSheet,
  TouchableHighlight,
  TouchableOpacity,
  StatusBar,
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
import distanceInMiles from "../utils/distance";
import { faBriefcase } from "@fortawesome/free-solid-svg-icons";
import capitalise from "../utils/capitalise";

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
      style={{ marginBottom: 6 }}
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
            {user.job && (
              <Text style={styles.role}>{capitalise(user.job)}</Text>
            )}
            {user.lat && (
              <View style={styles.distance}>
                <FontAwesomeIcon
                  style={styles.distancePin}
                  color={colors.grey}
                  icon={faLocationDot}
                  size={14}
                />
                <Text style={styles.distanceText}>
                  {distanceInMiles(
                    user.lat,
                    user.lon,
                    state.user.lat,
                    state.user.lon
                  )}{" "}
                  miles away
                </Text>
              </View>
            )}
          </View>
        </View>
        {/* <Text style={styles.bio}>{user.bio}</Text> */}
        <View style={styles.horizontalLine} />
        <View style={styles.cardBottom}>
          <View>
            <Text style={{ fontSize: 12 }}>
              <Text style={{ fontWeight: "bold" }}>19</Text> Students Helped
            </Text>
            <Text style={{ fontSize: 12 }}>
              <Text style={{ fontWeight: "bold" }}>6</Text> Languages
            </Text>
            <Text style={{ fontSize: 12 }}>
              <Text style={{ fontWeight: "bold" }}>2</Text> Years Industry
              Experience
            </Text>
          </View>

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
  name: {
    fontSize: 16,
    fontWeight: "bold",
    // textAlign: "center",
  },
  role: {
    fontSize: 14,
    color: colors.black,
    // textAlign: "center",
    marginTop: 2,
  },
  location: {
    fontSize: 12,
    color: colors.grey,
    flex: 1,
  },
  bio: {
    marginTop: 12,
    color: colors.grey,
    marginBottom: 4,
    // textAlign: "center",
    fontSize: 14,
  },
  profile: { width: 70, height: 70, borderRadius: 35, marginRight: 12 },
  card: {
    borderRadius: 0,
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
  distance: {
    fontWeight: "bold",
    color: colors.grey,
    fontSize: 14,
    flexDirection: "row",
    alignItems: "center",
    marginTop: 6,
  },
  distancePin: {
    marginRight: 6,
  },
  distanceText: {
    color: colors.grey,
  },
});

export default UserCard;
