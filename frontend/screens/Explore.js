import React from "react";
import { Text, View, TextInput, StyleSheet } from "react-native";
import Header from "../components/Header";
import Title from "../components/Title";
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
    </View>
  );
};

const styles = StyleSheet.create({
  input: {
    height: 45,
    marginHorizontal: 24,
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 20,
    color: colors.grey,
    borderColor: colors.stroke,
    fontSize: 14,
  },
});

export default Explore;
