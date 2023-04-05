import React, { useState, useContext } from "react";
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

const OnboardingPersonalDetails = ({ navigation }) => {
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");

	const { authContext, state } = useAuth();

	const handlePress = () => {
		authContext.updateDetails(state, {
			first_name: firstName,
			last_name: lastName,
		});
		navigation.navigate("OnboardingInterests");
	};

	return (
		<SafeAreaView
			style={{
				flex: 1,
				marginTop: StatusBar.currentHeight,
				paddingHorizontal: 24,
			}}
		>
			<Pressable onPress={() => authContext.signOut()}>
				<FontAwesomeIcon
					icon={faArrowLeft}
					style={{ marginTop: 24 }}
					size={24}
				/>
			</Pressable>

			<View style={styles.form}>
				<View style={{ flex: 1 }}>
					<Text style={styles.text}>Personal Details</Text>
					<TextInput
						onChangeText={setFirstName}
						value={firstName}
						placeholder="First name"
						style={[styles.input, globalStyles.shadowProp]}
					/>
					<TextInput
						onChangeText={setLastName}
						value={lastName}
						placeholder="Last name"
						style={[styles.input, globalStyles.shadowProp]}
					/>
				</View>

				<Pressable
					style={[
						styles.button,
						!(firstName && lastName) && styles.buttonDisabled,
					]}
					onPress={handlePress}
					disabled={!(firstName && lastName)}
				>
					<Text style={styles.buttonText}>Continue</Text>
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

export default OnboardingPersonalDetails;
