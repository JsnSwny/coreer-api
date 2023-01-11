import React from "react";
import { Text, View, TextInput, StyleSheet } from "react-native";
import Header from "../components/Header";
import Title from "../components/Title";
import UserCard from "../components/UserCard";
import colors from "../config/colors";

const Explore = () => {
  const [text, onChangeText] = React.useState("");
  return (
    <View>
      <Header />
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
        <UserCard
          user={{
            name: "John Doe",
            currentRole: "Software Engineer at Google",
            location: "Edinburgh, United Kingdom",
            image:
              "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
          }}
        />
      </View>
    </View>
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
