import React, { useState, useContext, useEffect } from "react";
import {
	Text,
	Pressable,
	SafeAreaView,
	View,
	StyleSheet,
	TextInput,
	Button,
	Image,
	StatusBar,
} from "react-native";
import Header from "../../components/Header";
import axios from "axios";
import colors from "../../config/colors";
import { useAuth } from "../../context/AuthContext";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import globalStyles from "../../config/globalStyles";
import Interests from "../../components/onboarding/Interests";
import { API_URL } from "@env";

const OnboardingLanguages = ({ navigation }) => {
	const { authContext, state } = useAuth();

	const [languages, setLanguages] = useState([]);
	useEffect(() => {
		axios
			.get(`${API_URL}/most-popular-languages/`)
			.then((res) => {
				setLanguages(res.data["languages"]);
			})
			.catch((err) => {
				console.log(err.response);
			});
	}, []);

	const [selectedLanguages, setSelectedLanguages] = useState([]);

	const handlePress = () => {
		authContext.updateDetails(state, {
			languages_id: selectedLanguages.map((item) => item.id),
		});
	};

	return (
		<SafeAreaView
			style={{
				flex: 1,
				marginTop: StatusBar.currentHeight,
				paddingHorizontal: 24,
			}}
		>
			<Pressable onPress={() => navigation.navigate("OnboardingInterests")}>
				<FontAwesomeIcon
					icon={faArrowLeft}
					style={{ marginTop: 24 }}
					size={24}
				/>
			</Pressable>

			<View style={styles.form}>
				<View style={{ flex: 1 }}>
					<Text style={styles.text}>Languages</Text>
					<Interests
						items={languages}
						selectedItems={selectedLanguages}
						setSelectedItems={setSelectedLanguages}
					/>
				</View>

				<Pressable
					style={[
						styles.button,
						selectedLanguages.length < 5 && styles.buttonDisabled,
					]}
					onPress={handlePress}
					disabled={selectedLanguages.length < 5}
				>
					<Text style={styles.buttonText}>
						Continue ({selectedLanguages.length} / 5)
					</Text>
				</Pressable>
			</View>
		</SafeAreaView>
	);
};

const styles = StyleSheet.create({
	navText: {
		textAlign: "center",
		color: colors.black,
	},
	separator: {
		width: "100%",
		borderBottomWidth: 1,
		borderBottomColor: colors.stroke,
		marginVertical: 24,
	},
	image: {
		alignItems: "center",
		justifyContent: "center",
		marginTop: 32,
	},
	text: {
		fontSize: 24,

		// fontFamily: "RalewayBold",
		marginBottom: 24,
	},
	form: {
		marginTop: 40,
		flex: 1,
	},
	input: {
		backgroundColor: "#fff",
		height: 50,
		borderWidth: 0.5,
		borderRadius: 10,
		paddingHorizontal: 20,
		color: colors.grey,
		borderColor: colors.stroke,
		fontSize: 14,
		marginBottom: 16,
	},
	button: {
		backgroundColor: colors.primary,

		alignItems: "center",
		justifyContent: "center",
		paddingVertical: 16,
		paddingHorizontal: 32,
		borderRadius: 100,
		marginBottom: 24,
	},
	buttonDisabled: {
		opacity: 0.5,
	},
	buttonText: {
		color: "#fff",
		fontSize: 16,
	},
});

export default OnboardingLanguages;
