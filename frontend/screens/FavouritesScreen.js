import axios from "axios";
import React, { useEffect, useState } from "react";
import { TextInput, View, Text, ScrollView } from "react-native";
import UserCard from "../components/UserCard";
import Header from "../components/Header";
import globalStyles from "../config/globalStyles";
import { useAuth } from "../context/AuthContext";
import Title from "../components/Title";
import { API_URLL as API_URL } from "@env";
import { useFocusEffect } from "@react-navigation/native";

const FavouritesScreen = ({ navigation }) => {
	const [results, setResults] = useState([]);
	const { state, dispatch } = useAuth();

	useFocusEffect(
		React.useCallback(() => {
			const config = {
				headers: {
					"Content-Type": "application/json",
				},
			};

			console.log("Getting followers");

			config.headers["Authorization"] = `Token ${state.userToken}`;
			axios
				.get(`${API_URL}/api/follow?ordering=-followed_on`, config)
				.then((res) => {
					console.log(res.data);
					setResults(res.data.map((item) => item.following));
				})
				.catch((err) => {
					console.log(err.response);
					return;
				});
		}, [])
	);

	return (
		<>
			<Header title={`Likes (${results.length})`} />
			<ScrollView contentContainerStyle={{ marginTop: 16 }}>
				{results.map((profile) => {
					return (
						<UserCard key={profile.id} navigation={navigation} user={profile} />
					);
				})}
			</ScrollView>
		</>
	);
};

export default FavouritesScreen;
