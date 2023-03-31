import axios from "axios";
import React, { useEffect, useState } from "react";
import {
	TextInput,
	View,
	Text,
	ScrollView,
	FlatList,
	ActivityIndicator,
} from "react-native";
import UserCard from "../components/UserCard";
import Header from "../components/Header";
import globalStyles from "../config/globalStyles";
import { API_URLL as API_URL } from "@env";
import colors from "../config/colors";

const SearchScreen = ({ route, navigation }) => {
	const { search } = route.params;
	const [results, setResults] = useState([]);
	const [searchInput, setSearchInput] = useState(search);

	const [page, setPage] = useState(1);
	const [perPage, setPerPage] = useState(10);
	const [totalResults, setTotalResults] = useState(0);
	const [isLoading, setIsLoading] = useState(false);
	const [hasMoreResults, setHasMoreResults] = useState(false);

	useEffect(() => {
		loadResults();
	}, []);

	const loadResults = () => {
		setIsLoading(true);

		axios
			.get(`${API_URL}/api/user/`, {
				params: {
					search: searchInput,
					page: page,
					perPage: perPage,
				},
			})
			.then((res) => {
				setResults(res.data.results);
				setHasMoreResults(!!res.data.next);
				setTotalResults(res.data.count);
			})
			.catch((error) => console.error(error))
			.finally(() => setIsLoading(false));
	};

	const loadMoreResults = () => {
		if (!isLoading && hasMoreResults) {
			setPage(page + 1);
			setIsLoading(true);

			axios
				.get(`${API_URL}/api/user/`, {
					params: {
						search: searchInput,
						page: page + 1,
						perPage: perPage,
					},
				})
				.then((res) => {
					setResults([...results, ...res.data.results]);
					setHasMoreResults(!!res.data.next);
					setTotalResults(res.data.count);
				})
				.catch((error) => console.error(error))
				.finally(() => setIsLoading(false));
		}
	};

	return (
		<>
			<Header backButton={true} title="Search" navigation={navigation} />

			<View style={{ paddingHorizontal: 16, paddingVertical: 16 }}>
				<Text style={{ marginBottom: 4, fontWeight: "bold" }}>
					{results.length} of {totalResults} result{results.length > 1 && "s"}{" "}
					for:
				</Text>
				<TextInput
					onChangeText={setSearchInput}
					value={searchInput}
					style={[globalStyles.input]}
					onSubmitEditing={() => {
						setPage(1);
						setResults([]);
						loadResults();
					}}
				/>
			</View>

			<FlatList
				data={results}
				renderItem={({ item }) => {
					return <UserCard key={item.id} navigation={navigation} user={item} />;
				}}
				keyExtractor={(item) => item.id.toString()}
				onEndReached={loadMoreResults}
				onEndReachedThreshold={0.2}
				ListHeaderComponent={<View />}
				ListFooterComponent={
					isLoading && <ActivityIndicator size="large" color={colors.primary} />
				}
			/>
		</>
	);
};

export default SearchScreen;
