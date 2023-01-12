import React from "react";
import { Text, View, Image, ScrollView, StyleSheet } from "react-native";
import Header from "../components/Header";
import ProfileBox from "../components/ProfileBox";
import colors from "../config/colors";

const Profile = ({ route, navigation }) => {
  const { user } = route.params;
  return (
    <React.Fragment>
      <View>
        <Header title={user.name} backButton={true} navigation={navigation} />
      </View>
      <View style={styles.headerCircle} />
      <ScrollView style={styles.container}>
        <ProfileBox navigation={navigation} user={user} />
      </ScrollView>
    </React.Fragment>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 16,
  },
  headerCircle: {
    width: "150%",
    height: 200,
    backgroundColor: colors.primary,
    position: "absolute",
    zIndex: -1,
  },
});

export default Profile;
