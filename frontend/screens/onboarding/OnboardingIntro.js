import React, { useState, useContext } from "react";
import {
  Text,
  Pressable,
  SafeAreaView,
  View,
  StyleSheet,
  TextInput,
  Button,
  Image,
} from "react-native";
import Header from "../../components/Header";
import axios from "axios";
import colors from "../../config/colors";
import { useAuth } from "../../context/AuthContext";

const OnboardingIntro = ({ navigation }) => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const handlePress = () => {
    login.signIn(email, password);
  };

  return (
    <SafeAreaView>
      <Header title="Coreer" />
      <Text style={styles.text}>Login</Text>
      <View style={styles.form}>
        <TextInput
          onChangeText={setFirstName}
          value={firstName}
          placeholder="First name"
          style={styles.input}
        />
        <TextInput
          secureTextEntry={true}
          onChangeText={setLastName}
          value={lastName}
          placeholder="Last name"
          style={styles.input}
        />
        <Pressable style={styles.button} onPress={handlePress}>
          <Text style={styles.buttonText}>Get Started</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  navText: {
    textAlign: "center",
    color: colors.black,
  },
  separator: {
    width: "100%",
    borderBottomWidth: 1,
    borderBottomColor: colors.stroke,
    marginVertical: 24,
  },
  image: {
    alignItems: "center",
    justifyContent: "center",
    marginTop: 32,
  },
  text: {
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 32,
    marginTop: 24,
  },
  form: {
    paddingHorizontal: 16,
    marginTop: 24,
  },
  input: {
    backgroundColor: "#fff",
    height: 50,
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 20,
    color: colors.grey,
    borderColor: colors.stroke,
    fontSize: 14,
    marginBottom: 16,
  },
  button: {
    backgroundColor: colors.primary,
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 10,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
});

export default OnboardingIntro;
