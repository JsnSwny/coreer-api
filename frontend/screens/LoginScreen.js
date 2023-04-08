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
} from "react-native";
import Header from "../components/Header";
import axios from "axios";
import colors from "../config/colors";
import { useAuth } from "../context/AuthContext";
import globalStyles from "../config/globalStyles";
import { SvgUri } from "react-native-svg";
import LoginVector from "../assets/LoginVector.svg";

const LoginScreen = ({ navigation }) => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const { authContext } = useAuth();

	const handlePress = () => {
		authContext.signIn(email, password);
	};

	return (
		<SafeAreaView>
			<Header title="coreer" />
			<View style={styles.image}>
				<LoginVector width={"100%"} />
			</View>

			<Text style={styles.text}>Login</Text>
			<View style={styles.form}>
				<TextInput
					onChangeText={setEmail}
					value={email}
					placeholder="Email"
					style={[globalStyles.input, styles.input]}
				/>
				<TextInput
					secureTextEntry={true}
					onChangeText={setPassword}
					value={password}
					placeholder="Password"
					style={[globalStyles.input, styles.input]}
				/>
				<Pressable style={styles.button} onPress={handlePress}>
					<Text style={styles.buttonText}>Login</Text>
				</Pressable>
				<View style={styles.separator} />
				<Text style={styles.navText}>
					Don't have an account?{" "}
					<Text
						onPress={() => navigation.navigate("Signup")}
						style={{ color: colors.primary, fontWeight: "bold" }}
					>
						Sign up
					</Text>
				</Text>
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
		textAlign: "center",
		fontWeight: "bold",
		fontSize: 32,
		marginTop: 24,
	},
	form: {
		paddingHorizontal: 16,
		marginTop: 24,
	},
	input: {
		marginBottom: 16,
	},
	button: {
		backgroundColor: colors.primary,
		borderRadius: 10,
		alignItems: "center",
		justifyContent: "center",
		paddingVertical: 12,
		paddingHorizontal: 32,
		borderRadius: 10,
	},
	buttonText: {
		color: "#fff",
		fontWeight: "bold",
	},
});

export default LoginScreen;
