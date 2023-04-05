import React from "react";
import { View, Image, Text, StyleSheet, TouchableOpacity } from "react-native";
import colors from "../config/colors";
import { format, isToday, isThisWeek, isSameYear, isSameDay } from "date-fns";

const InboxItem = ({ conversation, navigation }) => {
	const handlePress = () => {
		navigation.navigate("Messaging", { toUser: conversation.other_user });
	};

	const truncatedMessage = (message) => {
		return message.length > 30 ? `${message.substring(0, 30)}...` : message;
	};

	const getFormatString = (timestamp) => {
		timestamp = new Date(timestamp);
		let dateFormat = null;
		if (isToday(timestamp)) {
			dateFormat = "HH:mm";
		} else if (isThisWeek(timestamp)) {
			dateFormat = "eee";
		} else if (isSameYear(timestamp, new Date())) {
			dateFormat = "d MMM";
		} else {
			dateFormat = "d MMM yyyy";
		}

		return format(timestamp, dateFormat);
	};

	return (
		<TouchableOpacity onPress={handlePress}>
			<View style={styles.container}>
				<Image
					style={styles.image}
					source={{
						uri: `${conversation.other_user.profile_photo}`,
					}}
				/>
				<View>
					<Text style={styles.name}>{conversation.other_user.first_name}</Text>
					{conversation.last_message && (
						<Text style={styles.preview}>
							{truncatedMessage(conversation.last_message.content)} •{" "}
							{getFormatString(conversation.last_message.timestamp)}
						</Text>
					)}
				</View>
			</View>
		</TouchableOpacity>
	);
};

const styles = StyleSheet.create({
	container: {
		flexDirection: "row",
		alignItems: "center",
		paddingBottom: 8,
		marginBottom: 8,
	},
	image: { width: 50, height: 50, marginRight: 16, borderRadius: 35 },
	name: {
		fontWeight: "bold",
		fontSize: 14,
		color: colors.black,
	},
	preview: {
		color: colors.grey,
		fontSize: 12,
	},
});

export default InboxItem;
