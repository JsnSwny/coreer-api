import axios from "axios";
import React, { useEffect, useState } from "react";
import { TextInput, View, Text } from "react-native";
import UserCard from "../components/UserCard";
import Header from "../components/Header";
import globalStyles from "../config/globalStyles";

const SearchScreen = ({ route, navigation }) => {
  const { search } = route.params;
  const [results, setResults] = useState([]);
  const [searchInput, setSearchInput] = useState(search);
  useEffect(() => {
    axios
      .get(`http://192.168.0.14:8000/api/user/?search=${search}`)
      .then((res) => setResults(res.data));
  }, []);

  return (
    <>
      <Header backButton={true} title="Search" navigation={navigation} />

      <View
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
                .get(`http://192.168.0.14:8000/api/user/?search=${searchInput}`)
                .then((res) => setResults(res.data))
            }
          />
        </View>

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

export default SearchScreen;
