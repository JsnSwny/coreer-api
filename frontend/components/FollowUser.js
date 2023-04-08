import React from "react";
import { TouchableOpacity } from "react-native";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import colors from "../config/colors";
import { faStar } from "@fortawesome/free-solid-svg-icons";
import { faStar as farStar } from "@fortawesome/free-regular-svg-icons";
import { API_URL } from "@env";

const FollowUser = ({ user, getRecommendations }) => {
	const { state, dispatch } = useAuth();

	const likeUser = () => {
		const config = {
			headers: {
				"Content-Type": "application/json",
			},
		};

		config.headers["Authorization"] = `Token ${state.userToken}`;
		let newLikes = state.user.following;

		state.user.following.includes(user.id)
			? axios
					.delete(`${API_URL}/api/follow/`, {
						headers: {
							"Content-Type": "application/json",
							Authorization: `Token ${state.userToken}`,
						},
						data: { following_id: user.id },
					})
					.then((res) => {
						dispatch({
							type: "UPDATE_LIKES",
							likes: res.data.following,
						});
						getRecommendations();
					})

					.catch((err) => console.log("error"))
			: axios
					.post(
						`${API_URL}/api/follow/`,
						{
							following_id: user.id,
						},
						config
					)
					.then((res) => {
						dispatch({
							type: "UPDATE_LIKES",
							likes: res.data.following,
						});
						getRecommendations();
					})

					.catch((err) => console.log("error"));

		if (state.user.following.includes(user.id)) {
			newLikes = [...newLikes.filter((item) => item != user.id)];
		} else {
			newLikes.push(user.id);
		}

		state.user.following = newLikes;
	};
	return (
		<TouchableOpacity onPress={likeUser}>
			<FontAwesomeIcon
				color={
					state.user.following.includes(user.id) ? colors.primary : colors.black
				}
				icon={state.user.following.includes(user.id) ? faStar : farStar}
				size={24}
			/>
		</TouchableOpacity>
	);
};

export default FollowUser;
