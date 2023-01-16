import axios from "axios";
import React, { useEffect, useState } from "react";
import { TextInput, View, Text } from "react-native";
import UserCard from "../components/UserCard";
import Header from "../components/Header";
import globalStyles from "../config/globalStyles";
import { useAuthState } from "../context/AuthContext";
import Title from "../components/Title";
import { API_URL } from "@env";

const FavouritesScreen = ({ navigation }) => {
  const [results, setResults] = useState([]);
  const authState = useAuthState();

  useEffect(() => {
    console.log(authState.user.likes.toString());
    axios
      .get(`${API_URL}/api/user/?id__in=${authState.user.likes.toString()},`)
      .then((res) => setResults(res.data))
      .catch((err) => {
        console.log(err.response);
        return;
      });
  }, [authState]);

  return (
    <>
      <Header title="coreer" />
      <View>
        <Title
          title="Favourites"
          subtitle={`You have ${results.length} favourites`}
        />
      </View>
      <View
        style={{
          paddingHorizontal: 16,
        }}
      >
        {results.map((profile) => {
          return (
            <UserCard
              key={profile.id}
              navigation={navigation}
              user={{
                id: profile.id,
                first_name: profile.first_name,
                last_name: profile.last_name,
                currentRole: "Software Engineer at Google",
                location: "Edinburgh, United Kingdom",
                image:
                  "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
              }}
            />
          );
        })}
      </View>
    </>
  );
};

export default FavouritesScreen;
