import axios from "axios";
import React, { useState, useEffect } from "react";
import {
	Text,
	View,
	TextInput,
	StyleSheet,
	TouchableHighlight,
	Fragment,
	FlatList,
	ScrollView,
	StatusBar,
	RefreshControl,
	Image,
} from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import Header from "../components/Header";
import Navigation from "../components/Navigation";
import Title from "../components/Title";
import UserCard from "../components/UserCard";
import colors from "../config/colors";
import { useAuth } from "../context/AuthContext";
import { API_URLL as API_URL } from "@env";
import globalStyles from "../config/globalStyles";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import Languages from "../components/explore/Languages";
import * as SplashScreen from "expo-splash-screen";

const Explore = ({ navigation }) => {
	const [text, onChangeText] = React.useState("");
	const [profiles, setProfiles] = useState([]);
	const [popularLanguages, setPopularLanguages] = useState([]);
	const { state, dispatch } = useAuth();

	const searchSubmit = () => {
		navigation.navigate("Search", { search: text });
	};

	const [refreshing, setRefreshing] = React.useState(false);

	const getRecommendations = () => {
		setRefreshing(true);
		axios
			.get(`${API_URL}/recommend/10/${state.user.id}`)
			.then((res) => {
				setProfiles(res.data["recommendations"].slice(0, 50));
				setRefreshing(false);
				SplashScreen.hideAsync();
			})
			.catch((err) => {
				console.log("error");
				console.log(err.response);
			});
	};

	const onRefresh = React.useCallback(() => {
		getRecommendations();
	}, []);

	// useFocusEffect(
	// 	React.useCallback(() => {
	// 		getRecommendations();
	// 	}, [])
	// );

	useEffect(() => {
		getRecommendations();
		axios
			.get(`${API_URL}/most-popular-languages/`)
			.then((res) => {
				setPopularLanguages(res.data["languages"]);
			})
			.catch((err) => {
				console.log("error");
				console.log(err.response);
			});
	}, []);

	return (
		<React.Fragment>
			<View style={styles.banner}>
				<Text style={styles.bannerText}>Find a professional</Text>
				<View
					style={[globalStyles.shadowProp, globalStyles.input, styles.input]}
				>
					<FontAwesomeIcon
						icon={faSearch}
						color={colors.primary}
						style={{ marginRight: 12 }}
					/>
					<TextInput
						onChangeText={onChangeText}
						value={text}
						placeholder="Search (e.g., 'Glasgow web dev python')"
						onSubmitEditing={searchSubmit}
						clearButtonMode="while-editing"
						style={{ flex: 1, paddingVertical: 12 }}
					/>
				</View>
			</View>

			<ScrollView
				refreshControl={
					<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
				}
				// contentContainerStyle={{ paddingHorizontal: 16 }}
			>
				<View style={{ paddingHorizontal: 16 }}>
					<Title title="Popular languages" />
					<Languages languages={popularLanguages} navigation={navigation} />
				</View>

				<View style={{ paddingHorizontal: 16 }}>
					<Title
						title="Recommended for you"
						subtitle="The top matches based on your preferences"
					/>
				</View>
				<View>
					{profiles.map((profile) => {
						return (
							<UserCard
								key={profile.id}
								navigation={navigation}
								user={profile}
								getRecommendations={getRecommendations}
							/>
						);
					})}
				</View>
			</ScrollView>
		</React.Fragment>
	);
};

const styles = StyleSheet.create({
	banner: {
		paddingTop: StatusBar.currentHeight + 16,
		paddingHorizontal: 16,
		paddingBottom: 16,
		backgroundColor: colors.primary,
	},
	bannerText: {
		color: "white",
		fontWeight: "bold",
		fontSize: 18,
		marginBottom: 12,
	},
	input: {
		flexDirection: "row",
		alignItems: "center",
		borderColor: "transparent",
	},
});

export default Explore;
