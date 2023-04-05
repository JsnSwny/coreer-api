import { useContext } from "react";
import { View, Text, StyleSheet } from "react-native";
import colors from "../../config/colors";
import { AuthContext } from "../../context/AuthContext";
import { useAuth } from "../../context/AuthContext";
// import { MessageModel } from "../models/Message";

// export function classNames(...classes: any) {
//   return classes.filter(Boolean).join(" ");
// }

export function Message({ message }) {
	const { state, dispatch } = useAuth();

	function formatMessageTimestamp(timestamp) {
		const date = new Date(timestamp);
		return date.toLocaleTimeString().slice(0, 5);
	}
	const isFromUser = state.user.id == message.from_user.id;

	console.log("FROM USER");
	console.log(state.user.id);
	console.log(message.from_user.id);
	console.log(message.from_user.email);

	const styles = StyleSheet.create({
		container: {
			flex: 1,
			marginBottom: 16,
			justifyContent: "center",
			alignItems: isFromUser ? "flex-end" : "flex-start",
			paddingHorizontal: 16,
		},
		message: {
			maxWidth: "80%",
		},
		content: {
			backgroundColor: isFromUser ? colors.primary : "#fff",
			borderWidth: 0.5,
			borderColor: isFromUser ? "transparent" : colors.stroke,
			paddingHorizontal: 12,
			paddingVertical: 8,
			borderRadius: 10,
		},
		contentText: {
			color: isFromUser ? "#fff" : colors.black,
			lineHeight: 20,
		},
		timestamp: {
			color: colors.grey,
			marginTop: 4,
			marginLeft: 16,
			paddingRight: 8,
		},
	});

	return (
		<>
			<View style={styles.container}>
				<View style={styles.message}>
					<View style={styles.content}>
						<Text style={styles.contentText}>{message.content}</Text>
					</View>
					<Text style={styles.timestamp}>
						{formatMessageTimestamp(message.timestamp)}
					</Text>
				</View>
			</View>
		</>
	);
}
