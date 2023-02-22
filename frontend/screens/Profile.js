import React from "react";
import { Text, View, Image, ScrollView, StyleSheet } from "react-native";
import Header from "../components/Header";
import ProfileBox from "../components/ProfileBox";
import colors from "../config/colors";
import Languages from "../components/explore/Languages";
import Title from "../components/Title";
import globalStyles from "../config/globalStyles";

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
          // color={false}
        />
      </View>

      {/* <View style={styles.headerCircle}> */}
      {/* <View
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
        ></View> */}
      {/* <Image
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
        /> */}
      {/* </View> */}
      <ScrollView style={styles.container}>
        <ProfileBox navigation={navigation} user={user} />
        <View style={{ paddingVertical: 16 }}>
          <Title title="Languages" />
          <Languages languages={user.languages} />

          <Title title="Projects" />
          <View>
            <View style={[styles.project, globalStyles.shadowProp]}>
              <Image
                style={styles.projectImage}
                source={{
                  uri: "https://venngage-wordpress.s3.amazonaws.com/uploads/2020/08/Hopper-Landing-Page-Design.png",
                }}
              />
              <View style={styles.projectContainer}>
                <Text style={styles.projectTitle}>Coreer</Text>
                <Text style={styles.projectDescription}>
                  An application for connecting students and professionals
                  together
                </Text>
              </View>
            </View>
            <View style={[styles.project, globalStyles.shadowProp]}>
              <Image
                style={styles.projectImage}
                source={{
                  uri: "https://venngage-wordpress.s3.amazonaws.com/uploads/2020/08/Hopper-Landing-Page-Design.png",
                }}
              />
              <View style={styles.projectContainer}>
                <Text style={styles.projectTitle}>Coreer</Text>
                <Text style={styles.projectDescription}>
                  An application for connecting students and professionals
                  together
                </Text>
              </View>
            </View>
          </View>
        </View>
      </ScrollView>
    </React.Fragment>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 16,
  },
  projectImage: {
    height: 150,
    borderRadius: 10,
  },
  project: {
    width: "100%",
    backgroundColor: "white",
    borderWidth: 1,
    borderColor: colors.stroke,
    borderRadius: 10,
    marginBottom: 16,
  },
  projectContainer: {
    padding: 16,
  },
  projectTitle: {
    fontWeight: "bold",
    fontSize: 16,
    color: colors.black,
  },
  projectDescription: {
    marginTop: 8,
    color: colors.grey,
  },
  headerCircle: {
    width: "100%",
    height: 225,
    backgroundColor: colors.primary,
    position: "absolute",
    zIndex: -2,
    // borderBottomLeftRadius: 60,
    // borderBottomRightRadius: 60,
  },
});

export default Profile;
