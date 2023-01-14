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
import Header from "../components/Header";
import axios from "axios";
import colors from "../config/colors";
import { useAuth } from "../context/AuthContext";

const SignupScreen = ({ navigation }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

  const auth = useAuth();

  const handlePress = () => {
    auth.signUp({ email, password, passwordConfirm });
  };

  return (
    <SafeAreaView>
      <Header title="Coreer" />
      <View style={styles.image}>
        <Image source={require("../assets/login-vector.png")} />
      </View>
      <Text style={styles.text}>Sign Up</Text>
      <View style={styles.form}>
        <TextInput
          onChangeText={setEmail}
          value={email}
          placeholder="Email"
          style={styles.input}
        />
        <TextInput
          secureTextEntry={true}
          onChangeText={setPassword}
          value={password}
          placeholder="Password"
          style={styles.input}
        />
        <TextInput
          secureTextEntry={true}
          onChangeText={setPasswordConfirm}
          value={passwordConfirm}
          placeholder="Confirm Password"
          style={styles.input}
        />
        <Pressable style={styles.button} onPress={handlePress}>
          <Text style={styles.buttonText}>Sign Up</Text>
        </Pressable>
        <View style={styles.separator} />
        <Text style={styles.navText}>
          Already have an account?{" "}
          <Text
            onPress={() => navigation.navigate("Login")}
            style={{ color: colors.primary, fontWeight: "bold" }}
          >
            Login
          </Text>
        </Text>
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

export default SignupScreen;
