import React, { useState, useEffect, useCallback, useRef } from "react";
import {
	Text,
	StatusBar,
	View,
	StyleSheet,
	TouchableWithoutFeedback,
	TextInput,
	ScrollView,
	KeyboardAvoidingView,
} from "react-native";
import colors from "../config/colors";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { faArrowLeft, faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { API_URLL as API_URL } from "@env";
import { useAuth } from "../context/AuthContext";
import useWebSocket, { ReadyState } from "react-native-use-websocket";
import { Message } from "../components/chat/Message";

const MessagingScreen = ({ navigation, route }) => {
	const { toUser } = route.params;
	const [message, setMessage] = useState("");
	const scrollViewRef = useRef();

	const { state, dispatch } = useAuth();
	const userIds = [state.user.id, toUser.id].sort();
	const roomName = `${userIds[0]}__${userIds[1]}`;
	const [messageHistory, setMessageHistory] = useState([]);
	const { readyState } = useWebSocket(
		`ws://137.195.116.246:8000/ws/chat/${roomName}/`,
		{
			onMessage: (e) => {
				const data = JSON.parse(e.data);
				switch (data.type) {
					case "chat_message_echo":
						setMessageHistory((previous) => {
							console.log("CHAT MESSAGE ECHO");
							console.log([...previous, data.message]);
							return [...previous, data.message];
						});
						break;
					case "message_history":
						setMessageHistory(data.messages);
						break;
				}
			},
			onOpen: () => {
				console.log("Connected!");
			},
			onClose: () => {
				console.log("Disconnected!");
			},
		}
	);

	const { sendJsonMessage } = useWebSocket(
		`ws://137.195.116.246:8000/ws/chat/${roomName}/`
	);

	const sendMessage = () => {
		sendJsonMessage({
			type: "chat_message",
			message,
		});
		setMessage("");
	};
	return (
		<React.Fragment>
			<TouchableWithoutFeedback onPress={() => navigation.goBack()}>
				<View style={styles.container}>
					<FontAwesomeIcon
						icon={faArrowLeft}
						style={[styles.title, styles.back]}
					/>

					<Text style={styles.title}>Message {toUser.first_name}</Text>
				</View>
			</TouchableWithoutFeedback>
			<KeyboardAvoidingView style={{ flex: 1, paddingTop: 16 }}>
				<ScrollView
					ref={scrollViewRef}
					onContentSizeChange={() =>
						scrollViewRef.current.scrollToEnd({ animated: true })
					}
				>
					{messageHistory.map((message) => (
						<Message key={message.id} message={message} />
					))}
				</ScrollView>

				<View
					style={{
						justifyContent: "center",
						alignItems: "center",
						flexDirection: "row",
					}}
				>
					<TextInput
						style={styles.input}
						onChangeText={setMessage}
						text={message}
						value={message}
						placeholder="Type here..."
					/>
					{message.length > 0 && (
						<TouchableWithoutFeedback onPress={sendMessage}>
							<View>
								<FontAwesomeIcon
									icon={faPaperPlane}
									style={{ marginRight: 16, zIndex: 100 }}
									size={20}
									color={colors.primary}
								/>
							</View>
						</TouchableWithoutFeedback>
					)}
				</View>
			</KeyboardAvoidingView>
		</React.Fragment>
	);
};

const styles = StyleSheet.create({
	container: {
		backgroundColor: colors.primary,
		paddingTop: StatusBar.currentHeight + 16,
		paddingBottom: 16,
		paddingHorizontal: 16,
		flexDirection: "row",
		alignItems: "center",
	},
	input: {
		borderRadius: 25,
		height: 35,
		paddingHorizontal: 16,
		backgroundColor: "#fff",
		flex: 1,
		margin: 16,
		borderWidth: 0.5,
		borderColor: colors.stroke,
	},
	title: {
		color: "#fff",
		fontWeight: "bold",
		fontSize: 16,
	},
	back: {
		marginRight: 8,
	},
});

export default MessagingScreen;
