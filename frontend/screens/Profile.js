import React, { useEffect } from "react";
import { Text, View, Image, ScrollView, StyleSheet } from "react-native";
import Header from "../components/Header";
import ProfileBox from "../components/ProfileBox";
import colors from "../config/colors";
import Languages from "../components/explore/Languages";
import Title from "../components/Title";
import globalStyles from "../config/globalStyles";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import { API_URL } from "@env";

const Profile = ({ route, navigation }) => {
	const { user } = route.params;
	const { state } = useAuth();
	useEffect(() => {
		const config = {
			headers: {
				"Content-Type": "application/json",
			},
		};

		config.headers["Authorization"] = `Token ${state.userToken}`;
		const data = { from_user: state.user.id, to_user: user.id };
		axios.post(`${API_URL}/api/recommendations/`, data, config);
	}, []);
	return (
		<React.Fragment>
			<View>
				<Header title={user.name} backButton={true} navigation={navigation} />
			</View>
			<ScrollView style={styles.container}>
				<ProfileBox navigation={navigation} user={user} />
				<View style={{ paddingVertical: 16 }}>
					<Title title="Languages" />
					<Languages languages={user.languages} />

					<Title title="Projects" />
					<View>
						{user.projects.map((project) => (
							<View style={[styles.project, globalStyles.shadowProp]}>
								{project.image && (
									<Image
										style={styles.projectImage}
										source={{
											uri: "https://venngage-wordpress.s3.amazonaws.com/uploads/2020/08/Hopper-Landing-Page-Design.png",
										}}
									/>
								)}

								<View style={styles.projectContainer}>
									<Text style={styles.projectTitle}>
										{project.title.split("/").pop()}
									</Text>
									<Text style={styles.projectDescription}>
										{project.description}
									</Text>
								</View>
							</View>
						))}
					</View>
				</View>
			</ScrollView>
		</React.Fragment>
	);
};

const styles = StyleSheet.create({
	container: {
		paddingHorizontal: 16,
	},
	projectImage: {
		height: 150,
		borderRadius: 10,
	},
	project: {
		width: "100%",
		backgroundColor: "white",
		borderWidth: 1,
		borderColor: colors.stroke,
		borderRadius: 10,
		marginBottom: 16,
	},
	projectContainer: {
		padding: 16,
	},
	projectTitle: {
		fontWeight: "bold",
		fontSize: 16,
		color: colors.black,
	},
	projectDescription: {
		marginTop: 8,
		color: colors.grey,
	},
	headerCircle: {
		width: "100%",
		height: 225,
		backgroundColor: colors.primary,
		position: "absolute",
		zIndex: -2,
		// borderBottomLeftRadius: 60,
		// borderBottomRightRadius: 60,
	},
});

export default Profile;
