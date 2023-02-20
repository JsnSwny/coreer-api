import React from "react";
import { ScrollView, Image, Text, View, StyleSheet } from "react-native";
import colors from "../../config/colors";
import Title from "../Title";
import { SvgUri } from "react-native-svg";

const Languages = ({ languages = [] }) => {
  return (
    <View style={{ marginBottom: 16 }}>
      <ScrollView horizontal={true} showsHorizontalScrollIndicator={false}>
        {languages.map((language) => (
          <View style={[styles.languageBox]}>
            {console.log(language)}
            <View style={{ flex: 1 }}>
              {console.log(
                `https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/${language.icon_name.toLowerCase()}/${language.icon_name.toLowerCase()}-original.svg`
              )}
              <SvgUri
                style={styles.languageImage}
                uri={`https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/${language.icon_name.toLowerCase()}/${language.icon_name.toLowerCase()}-original.svg`}
              />
            </View>

            <Text style={styles.languageText}>{language.name}</Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  languageBox: {
    backgroundColor: "white",
    height: 100,
    width: 120,
    borderWidth: 1,
    borderColor: colors.stroke,
    marginRight: 8,
    borderRadius: 15,
    padding: 16,
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  languageImage: {
    width: 35,
    height: 35,
  },
  languageText: {
    fontWeight: "bold",
    marginTop: 12,
    fontSize: 14,
  },
});

export default Languages;
