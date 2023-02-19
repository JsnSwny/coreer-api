import axios from "axios";
import React, { useEffect, useState } from "react";
import { TextInput, View, Text, ScrollView } from "react-native";
import UserCard from "../components/UserCard";
import Header from "../components/Header";
import globalStyles from "../config/globalStyles";
import { API_URLL as API_URL } from "@env";

const SearchScreen = ({ route, navigation }) => {
  const { search } = route.params;
  const [results, setResults] = useState([]);
  const [searchInput, setSearchInput] = useState(search);
  useEffect(() => {
    axios
      .get(`${API_URL}/api/user/?search=${search}`)
      .then((res) => setResults(res.data));
  }, [search]);

  return (
    <>
      <Header backButton={true} title="Search" navigation={navigation} />

      <ScrollView
        style={{
          paddingHorizontal: 16,
          marginTop: 16,
        }}
      >
        <View>
          <Text style={{ marginBottom: 4, fontWeight: "bold" }}>
            {results.length} result{results.length > 1 && "s"} for:
          </Text>
          <TextInput
            onChangeText={setSearchInput}
            value={searchInput}
            style={[globalStyles.input, { marginBottom: 16 }]}
            onSubmitEditing={() =>
              axios
                .get(`${API_URL}/api/user/?search=${searchInput}`)
                .then((res) => setResults(res.data))
            }
          />
        </View>

        {results.map((profile) => {
          return (
            <UserCard key={profile.id} navigation={navigation} user={profile} />
          );
        })}
      </ScrollView>
    </>
  );
};

export default SearchScreen;
