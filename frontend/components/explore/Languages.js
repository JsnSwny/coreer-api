import React from "react";
import {
	ScrollView,
	Image,
	Text,
	View,
	StyleSheet,
	Pressable,
} from "react-native";
import colors from "../../config/colors";
import Title from "../Title";
import { SvgUri } from "react-native-svg";

const Languages = ({ navigation, languages = [] }) => {
	return (
		<View style={{ marginBottom: 16 }}>
			<ScrollView horizontal={true} showsHorizontalScrollIndicator={false}>
				{languages.map((language) => (
					<Pressable
						style={[styles.languageBox]}
						onPress={() =>
							navigation.navigate("Search", { search: language.name })
						}
					>
						<View style={{ flex: 1 }}>
							<SvgUri
								style={styles.languageImage}
								uri={`https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/${language.icon_name.toLowerCase()}/${language.icon_name.toLowerCase()}-original.svg`}
							/>
						</View>

						<Text style={styles.languageText}>{language.name}</Text>
					</Pressable>
				))}
			</ScrollView>
		</View>
	);
};

const styles = StyleSheet.create({
	languageBox: {
		backgroundColor: "white",
		height: 100,
		width: 120,
		borderWidth: 1,
		borderColor: colors.stroke,
		marginRight: 8,
		borderRadius: 15,
		padding: 16,
		flex: 1,
		justifyContent: "center",
		alignItems: "center",
	},
	languageImage: {
		width: 35,
		height: 35,
	},
	languageText: {
		fontWeight: "bold",
		marginTop: 12,
		fontSize: 14,
	},
});

export default Languages;
