import React, { useState } from "react";
import {
  Text,
  StatusBar,
  View,
  StyleSheet,
  TouchableWithoutFeedback,
  TextInput,
} from "react-native";
import colors from "../config/colors";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";

const MessagingScreen = ({ navigation, route }) => {
  const { user } = route.params;
  const [message, setMessage] = useState("");
  return (
    <React.Fragment>
      <TouchableWithoutFeedback onPress={() => navigation.goBack()}>
        <View style={styles.container}>
          <FontAwesomeIcon
            icon={faArrowLeft}
            style={[styles.title, styles.back]}
          />

          <Text style={styles.title}>Message {user.name}</Text>
        </View>
      </TouchableWithoutFeedback>
      <View
        style={{
          justifyContent: "center",
          alignItems: "center",
          flex: 1,
        }}
      >
        <TextInput
          style={styles.input}
          onChangeText={setMessage}
          text={message}
          placeholder="Type here..."
        />
      </View>
    </React.Fragment>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.primary,
    paddingTop: StatusBar.currentHeight + 16,
    paddingBottom: 16,
    paddingHorizontal: 16,
    flexDirection: "row",
    alignItems: "center",
  },
  input: {
    borderColor: colors.primary,
    borderWidth: 2,
    borderRadius: 25,
    width: "90%",
    position: "absolute",
    bottom: 16,
    height: 50,
    paddingHorizontal: 16,
    backgroundColor: "#fff",
  },
  title: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 16,
  },
  back: {
    marginRight: 8,
  },
});

export default MessagingScreen;
