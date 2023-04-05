import React, { useState } from "react";
import { Text, View, StyleSheet } from "react-native";
import Title from "../components/Title";
import Header from "../components/Header";
import Navigation from "../components/Navigation";
import colors from "../config/colors";
import InboxItem from "../components/InboxItem";
import { useFocusEffect } from "@react-navigation/native";
import axios from "axios";
import { API_URL } from "@env";

import { useAuth } from "../context/AuthContext";
const Inbox = ({ navigation }) => {
	const { state } = useAuth();
	const [conversations, setConversations] = useState([]);
	useFocusEffect(
		React.useCallback(() => {
			const config = {
				headers: {
					"Content-Type": "application/json",
				},
			};

			config.headers["Authorization"] = `Token ${state.userToken}`;
			axios
				.get(`${API_URL}/api/conversations/`, config)
				.then((res) => {
					setConversations(res.data);
				})
				.catch((err) => console.log(err));
		}, [])
	);
	return (
		<>
			<Header title="Inbox" />
			<View
				style={{
					paddingHorizontal: 16,
					marginTop: 24,
				}}
			>
				{conversations.map((conversation) => (
					<>
						<InboxItem conversation={conversation} navigation={navigation} />
					</>
				))}
			</View>
		</>
	);
};

const styles = StyleSheet.create({});

export default Inbox;
