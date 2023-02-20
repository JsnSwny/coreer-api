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
  StatusBar,
  RefreshControl,
  Image,
} from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import Header from "../components/Header";
import Navigation from "../components/Navigation";
import Title from "../components/Title";
import UserCard from "../components/UserCard";
import colors from "../config/colors";
import { useAuth } from "../context/AuthContext";
import { API_URLL as API_URL } from "@env";
import globalStyles from "../config/globalStyles";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";

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
      {/* <Header title="coreer" /> */}
      <View style={styles.banner}>
        <Text style={styles.bannerText}>Find a professional</Text>
        <View
          style={[globalStyles.shadowProp, globalStyles.input, styles.input]}
        >
          <FontAwesomeIcon
            icon={faSearch}
            color={colors.primary}
            style={{ marginRight: 12 }}
          />
          <TextInput
            onChangeText={onChangeText}
            value={text}
            placeholder="Search professionals"
            onSubmitEditing={searchSubmit}
            clearButtonMode="while-editing"
            style={{ flex: 1, paddingVertical: 12 }}
          />
        </View>
      </View>

      <ScrollView
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        // contentContainerStyle={{ paddingHorizontal: 16 }}
      >
        <View style={{ paddingHorizontal: 16, marginBottom: 16 }}>
          <Title
            title="Popular languages"
            // subtitle="The top matches based on your preferences"
          />
          <ScrollView horizontal={true} showsHorizontalScrollIndicator={false}>
            <View style={[styles.languageBox]}>
              <View style={{ flex: 1 }}>
                <Image
                  style={styles.languageImage}
                  source={require("../assets/python-logo.png")}
                />
              </View>

              <Text style={styles.languageText}>Python</Text>
            </View>
            <View style={[styles.languageBox]}>
              <View style={{ flex: 1 }}>
                <Image
                  style={styles.languageImage}
                  source={require("../assets/js-logo.png")}
                />
              </View>

              <Text style={styles.languageText}>JavaScript</Text>
            </View>
            <View style={[styles.languageBox]}>
              <View style={{ flex: 1 }}>
                <Image
                  style={styles.languageImage}
                  source={require("../assets/java-logo.png")}
                />
              </View>

              <Text style={styles.languageText}>Java</Text>
            </View>
            <View style={[styles.languageBox]}>
              <View style={{ flex: 1 }}>
                <Image
                  style={styles.languageImage}
                  source={require("../assets/c-logo.png")}
                />
              </View>

              <Text style={styles.languageText}>C</Text>
            </View>
          </ScrollView>
        </View>

        <View style={{ paddingHorizontal: 16 }}>
          <Title
            title="Recommended for you"
            subtitle="The top matches based on your preferences"
          />
        </View>
        <View>
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
  banner: {
    paddingTop: StatusBar.currentHeight + 16,
    paddingHorizontal: 16,
    paddingBottom: 16,
    backgroundColor: colors.primary,
  },
  bannerText: {
    color: "white",
    fontWeight: "bold",
    fontSize: 18,
    marginBottom: 12,
  },
  input: {
    flexDirection: "row",
    alignItems: "center",
  },
  languageBox: {
    backgroundColor: "white",
    height: 100,
    width: 120,
    borderWidth: 1,
    borderColor: colors.stroke,
    marginRight: 8,
    borderRadius: 15,
    padding: 16,
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  languageImage: {
    width: 40,
    height: 40,
  },
  languageText: {
    fontWeight: "bold",
    marginTop: 12,
    fontSize: 14,
  },
});

export default Explore;
