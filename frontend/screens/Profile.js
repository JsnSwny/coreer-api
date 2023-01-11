import React from "react";
import { Text, View } from "react-native";
import Header from "../components/Header";

const Profile = ({ navigation }) => {
  return (
    <View>
      <Header title="John Doe" backButton={true} navigation={navigation} />
    </View>
  );
};

export default Profile;
