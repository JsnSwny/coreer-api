import React from "react";
import { Text, View, Button } from "react-native";
import Title from "../components/Title";
import Header from "../components/Header";
import Navigation from "../components/Navigation";
import { useAuth } from "../context/AuthContext";

const Account = ({ navigation }) => {
  const auth = useAuth();
  return (
    <React.Fragment>
      <Header title="coreer" />
      <View>
        <Title title="Account" />
      </View>
      <Button title="Log out" onPress={() => auth.signOut()} />
    </React.Fragment>
  );
};

export default Account;
