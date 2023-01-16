import React, { useState } from "react";
import { Text, View, StyleSheet } from "react-native";
import Title from "../components/Title";
import Header from "../components/Header";
import Navigation from "../components/Navigation";
import colors from "../config/colors";
import InboxItem from "../components/InboxItem";

const Inbox = ({ navigation }) => {
  return (
    <>
      <Header title="coreer" />
      <View>
        <Title title="Inbox" />
      </View>
      <View
        style={{
          paddingHorizontal: 16,
        }}
      >
        <InboxItem />
      </View>
    </>
  );
};

const styles = StyleSheet.create({});

export default Inbox;
