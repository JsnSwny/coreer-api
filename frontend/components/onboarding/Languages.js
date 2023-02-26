import React from "react";
import {
  View,
  Pressable,
  Text,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import colors from "../../config/colors";
import globalStyles from "../../config/globalStyles";

const Languages = ({ interests, selectedInterests, setSelectedInterests }) => {
  return (
    <View style={styles.interests}>
      {interests.map((interest) => {
        let selected = selectedInterests.some((item) => item == interest);
        return (
          <TouchableOpacity
            style={[
              styles.interest,
              globalStyles.shadowProp,
              selected && styles.interestHighlight,
            ]}
            onPress={() =>
              setSelectedInterests([...selectedInterests, interest])
            }
          >
            <Text
              style={{ fontSize: 10, color: selected ? "white" : colors.black }}
            >
              {interest}
            </Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  interests: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginRight: -8,
  },
  interest: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: "white",
    width: "auto",
    marginRight: 8,
    marginBottom: 8,
    borderRadius: 10,
  },
  interestHighlight: {
    backgroundColor: colors.primary,
  },
});

export default Languages;
