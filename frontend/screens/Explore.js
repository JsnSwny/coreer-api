import axios from "axios";
import React, { useState, useEffect } from "react";
import {
  Text,
  View,
  TextInput,
  StyleSheet,
  TouchableHighlight,
  Fragment,
  FlatList,
  ScrollView,
  RefreshControl,
} from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import Header from "../components/Header";
import Navigation from "../components/Navigation";
import Title from "../components/Title";
import UserCard from "../components/UserCard";
import colors from "../config/colors";
import { useAuth } from "../context/AuthContext";
import { API_URLL as API_URL } from "@env";

const Explore = ({ navigation }) => {
  const [text, onChangeText] = React.useState("");
  const [profiles, setProfiles] = useState([]);
  const { state, dispatch } = useAuth();

  const searchSubmit = () => {
    navigation.navigate("Search", { search: text });
  };

  const [refreshing, setRefreshing] = React.useState(false);

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    axios
      .get(`${API_URL}/recommend/${state.user.id}`)
      .then((res) => {
        console.log(
          res.data["recommendations"].slice(0, 50).map((item) => item.following)
        );
        setProfiles(res.data["recommendations"].slice(0, 50));
        setRefreshing(false);
      })
      .catch((err) => {
        console.log("error");
        console.log(err.response);
      });
  }, []);

  useFocusEffect(
    React.useCallback(() => {
      axios
        .get(`${API_URL}/recommend/${state.user.id}`)
        .then((res) => {
          console.log(
            res.data["recommendations"]
              .slice(0, 50)
              .map((item) => item.following)
          );
          setProfiles(res.data["recommendations"].slice(0, 50));
        })
        .catch((err) => {
          console.log("error");
          console.log(err.response);
        });
    }, [])
  );

  return (
    <React.Fragment>
      <Header title="coreer" />
      <ScrollView
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        <View>
          <Title
            title="Explore"
            subtitle="Search for an individual, career or industry"
          />
          <TextInput
            style={styles.input}
            onChangeText={onChangeText}
            value={text}
            placeholder="E.g., ‘Software Engineer’"
            onSubmitEditing={searchSubmit}
            clearButtonMode="while-editing"
          />
        </View>
        <View>
          <Title
            title="Recommended"
            subtitle="The top matches based on your preferences"
          />
        </View>
        <View
          style={{
            paddingHorizontal: 16,
          }}
        >
          {profiles.map((profile) => {
            return (
              <UserCard
                key={profile.id}
                navigation={navigation}
                user={profile}
              />
            );
          })}
        </View>
      </ScrollView>
    </React.Fragment>
  );
};

const styles = StyleSheet.create({
  input: {
    backgroundColor: "#fff",
    height: 45,
    marginHorizontal: 16,
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 20,
    color: colors.grey,
    borderColor: colors.stroke,
    fontSize: 14,
  },
});

export default Explore;
