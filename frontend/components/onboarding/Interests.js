import React from "react";
import {
  View,
  Pressable,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import colors from "../../config/colors";
import globalStyles from "../../config/globalStyles";
import { SvgUri } from "react-native-svg";

const Interests = ({ items, selectedItems, setSelectedItems }) => {
  return (
    <ScrollView contentContainerStyle={{ paddingHorizontal: 0 }}>
      <View style={styles.interests}>
        {items.map((item) => {
          let selected = selectedItems.some(
            (selectedItem) => item.id == selectedItem.id
          );
          return (
            <TouchableOpacity
              key={item.id}
              style={[
                styles.interest,
                globalStyles.shadowProp,
                selected && styles.interestHighlight,
              ]}
              onPress={() =>
                selected
                  ? setSelectedItems([
                      ...selectedItems.filter(
                        (selectedItem) => selectedItem.id != item.id
                      ),
                    ])
                  : setSelectedItems([...selectedItems, item])
              }
            >
              {item.icon_name && (
                <SvgUri
                  style={{ width: 12, height: 12, marginRight: 6 }}
                  uri={`https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/${item.icon_name.toLowerCase()}/${item.icon_name.toLowerCase()}-original.svg`}
                />
              )}

              <Text
                style={{
                  fontSize: 12,
                  color: selected ? "white" : colors.black,
                }}
              >
                {item.name}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </ScrollView>
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
    marginRight: 4,
    marginBottom: 4,
    borderRadius: 10,
    flexDirection: "row",
    alignItems: "center",
  },
  interestHighlight: {
    backgroundColor: colors.primary,
  },
});

export default Interests;
