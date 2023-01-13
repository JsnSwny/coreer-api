import React, { useContext, useState } from "react";
import axios from "axios";
import * as SecureStore from "expo-secure-store";

const AuthContext = React.createContext();
const AuthState = React.createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const useAuthState = () => {
  return useContext(AuthState);
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = React.useReducer(
    (prevState, action) => {
      switch (action.type) {
        case "RESTORE_TOKEN":
          return {
            ...prevState,
            userToken: action.token,
            isLoading: false,
          };
        case "SIGN_IN":
          return {
            ...prevState,
            isSignout: false,
            userToken: action.token,
          };
        case "SIGN_OUT":
          return {
            ...prevState,
            isSignout: true,
            userToken: null,
          };
      }
    },
    {
      isLoading: true,
      isSignout: false,
      userToken: null,
    }
  );

  React.useEffect(() => {
    // Fetch the token from storage then navigate to our appropriate place
    const bootstrapAsync = async () => {
      let userToken;

      try {
        userToken = await SecureStore.getItemAsync("userToken");
      } catch (e) {
        console.log("error");
        console.log(e.response);
        return;
      }
      // After restoring token, we may need to validate it in production apps

      // This will switch to the App screen or Auth screen and this loading
      // screen will be unmounted and thrown away.
      dispatch({ type: "RESTORE_TOKEN", token: userToken });
    };

    bootstrapAsync();
  }, []);

  const authContext = React.useMemo(
    () => ({
      signIn: async (username, password) => {
        console.log(username, password);
        const config = {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        };

        // Request Body
        const body = JSON.stringify({ username, password });
        axios
          .post("http://192.168.1.125:8000/api/auth/login", body, config)
          .then((res) => {
            console.log(`Logged in`);
            SecureStore.setItemAsync("userToken", res.data.token);
            dispatch({ type: "SIGN_IN", token: res.data.token });
          })
          .catch((err) => {
            console.log("error");
            console.log(err);
            return;
          });
      },
      signOut: () => dispatch({ type: "SIGN_OUT" }),
      signUp: async (data) => {
        // In a production app, we need to send user data to server and get a token
        // We will also need to handle errors if sign up failed
        // After getting token, we need to persist the token using `SecureStore`
        // In the example, we'll use a dummy token

        dispatch({ type: "SIGN_IN", token: "dummy-auth-token" });
      },
    }),
    []
  );

  return (
    <AuthContext.Provider value={authContext}>
      <AuthState.Provider value={state}>{children}</AuthState.Provider>
    </AuthContext.Provider>
  );
};
