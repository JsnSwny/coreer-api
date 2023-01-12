import React from "react";
import { Text, View } from "react-native";
import Title from "../components/Title";
import Header from "../components/Header";
import Navigation from "../components/Navigation";

const Account = ({ navigation }) => {
  return (
    <React.Fragment>
      <Header title="coreer" />
      <View>
        <Title title="Account" />
      </View>
      <Navigation navigation={navigation} />
    </React.Fragment>
  );
};

export default Account;
