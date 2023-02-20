import React from "react";
import { Text, View, Image, ScrollView, StyleSheet } from "react-native";
import Header from "../components/Header";
import ProfileBox from "../components/ProfileBox";
import colors from "../config/colors";
import Languages from "../components/explore/Languages";
import Title from "../components/Title";

const Profile = ({ route, navigation }) => {
  const { user } = route.params;
  console.log(user);
  return (
    <React.Fragment>
      <View>
        <Header
          title={user.name}
          backButton={true}
          navigation={navigation}
          color={false}
        />
      </View>

      <View style={styles.headerCircle}>
        <View
          style={{
            backgroundColor: "black",
            zIndex: 2,
            width: "100%",
            position: "absolute",
            top: 0,
            right: 0,
            bottom: 0,
            right: 0,
            opacity: 0.4,
            borderBottomLeftRadius: 60,
            borderBottomRightRadius: 60,
          }}
        ></View>
        <Image
          style={{
            width: "100%",
            height: 225,
            zIndex: -5,
            resizeMode: "cover",
            borderBottomLeftRadius: 60,
            borderBottomRightRadius: 60,
          }}
          source={{
            uri: "https://images.pexels.com/photos/6804610/pexels-photo-6804610.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
          }}
        />
      </View>
      <ScrollView style={styles.container}>
        <ProfileBox navigation={navigation} user={user} />
        <Title title="Languages" />
        <Languages languages={user.languages} />

        <Title title="Projects" />
        <Languages languages={user.languages} />
      </ScrollView>
    </React.Fragment>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 16,
  },
  headerCircle: {
    width: "100%",
    height: 225,
    backgroundColor: colors.primary,
    position: "absolute",
    zIndex: -2,
    borderBottomLeftRadius: 60,
    borderBottomRightRadius: 60,
  },
});

export default Profile;
