import axios from "axios";
import React, { useEffect, useState } from "react";
import { TextInput, View, Text, ScrollView } from "react-native";
import UserCard from "../components/UserCard";
import Header from "../components/Header";
import globalStyles from "../config/globalStyles";
import { useAuth } from "../context/AuthContext";
import Title from "../components/Title";
import { API_URLL as API_URL } from "@env";

const FavouritesScreen = ({ navigation }) => {
	const [results, setResults] = useState([]);
	const { state, dispatch } = useAuth();

	useEffect(() => {
		axios
			.get(`${API_URL}/api/user/?id__in=${state.user.following.toString()},`)
			.then((res) => {
				console.log(res);
				setResults(res.data.results);
			})
			.catch((err) => {
				console.log(err.response);
				return;
			});
	}, [state]);

	return (
		<>
			<Header title={`Favourites (${results.length})`} />
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
