import React from "react";
import {
  Text,
  View,
  TextInput,
  StyleSheet,
  TouchableHighlight,
  Fragment,
  FlatList,
  ScrollView,
} from "react-native";
import Header from "../components/Header";
import Navigation from "../components/Navigation";
import Title from "../components/Title";
import UserCard from "../components/UserCard";
import colors from "../config/colors";

const Explore = ({ navigation }) => {
  const [text, onChangeText] = React.useState("");

  const DATA = [
    {
      id: "bd7acbea-c1b1-46c2-aed5-3ad53abb28ba",
      name: "John Doe",
      role: "Software Engineer at Google",
      location: "Edinburgh, United Kingdom",
      image:
        "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    },
    {
      id: "bd7acbea-c1b1-46c2-aed5-3ad53abb28bb",
      name: "Jane Doe",
      role: "Software Engineer at Google",
      location: "Edinburgh, United Kingdom",
      image:
        "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    },
    {
      id: "bd7acbea-c1b1-46c2-aed5-3ad53abb28bc",
      name: "Bob Marley",
      role: "Software Engineer at Google",
      location: "Edinburgh, United Kingdom",
      image:
        "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
    },
  ];

  return (
    <React.Fragment>
      <Header title="coreer" />
      <ScrollView>
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
        {/* <FlatList
        data={DATA}
        renderItem={({ item }) => (
          <UserCard
            navigation={navigation}
            user={{
              name: item.name,
              currentRole: item.currentRole,
              location: item.location,
              image: item.image,
            }}
          />
        )}
        keyExtractor={(item) => item.id}
      /> */}
        <View
          style={{
            paddingHorizontal: 16,
            paddingBottom: 72,
          }}
        >
          <UserCard
            navigation={navigation}
            user={{
              name: "John Doe",
              currentRole: "Software Engineer at Google",
              location: "Edinburgh, United Kingdom",
              image:
                "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            }}
          />
          <UserCard
            navigation={navigation}
            user={{
              name: "Jane Doe",
              currentRole: "Lead Designer at Microsoft",
              location: "Edinburgh, United Kingdom",
              image:
                "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            }}
          />
          <UserCard
            navigation={navigation}
            user={{
              name: "Jane Doe",
              currentRole: "Lead Designer at Microsoft",
              location: "Edinburgh, United Kingdom",
              image:
                "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
            }}
          />
        </View>
      </ScrollView>
      <Navigation navigation={navigation} />
    </React.Fragment>
  );
};

const styles = StyleSheet.create({
  input: {
    backgroundColor: "#fff",
    height: 45,
    marginHorizontal: 16,
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 20,
    color: colors.grey,
    borderColor: colors.stroke,
    fontSize: 14,
  },
});

export default Explore;
