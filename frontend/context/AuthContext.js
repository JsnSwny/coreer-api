import React, { useContext, useState } from "react";
import axios from "axios";
import * as SecureStore from "expo-secure-store";

const AuthContext = React.createContext();
const AuthState = React.createContext();
const AuthDispatch = React.createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const useAuthState = () => {
  return useContext(AuthState);
};

export const useAuthDispatch = () => {
  return useContext(AuthDispatch);
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = React.useReducer(
    (prevState, action) => {
      switch (action.type) {
        case "RESTORE_TOKEN":
          return {
            ...prevState,
            userToken: action.token,
            user: action.user,
            isLoading: false,
          };
        case "UPDATE_USER":
          return {
            ...prevState,
            user: action.user,
          };
        case "UPDATE_LIKES":
          return {
            ...prevState,
            user: { ...prevState.user, likes: action.likes },
          };
        case "SIGN_IN":
          console.log("SIGNING IN");
          console.log(action.user);
          return {
            ...prevState,
            isSignout: false,
            userToken: action.token,
            user: action.user,
          };
        case "SIGN_OUT":
          return {
            ...prevState,
            isSignout: true,
            userToken: null,
            user: null,
          };
      }
    },
    {
      isLoading: true,
      isSignout: false,
      userToken: null,
      user: null,
    }
  );

  React.useEffect(() => {
    // Fetch the token from storage then navigate to our appropriate place
    const bootstrapAsync = async () => {
      let userToken;

      try {
        userToken = await SecureStore.getItemAsync("userToken");
      } catch (e) {
        console.log(e.response);
        return;
      }

      const config = {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      };

      config.headers["Authorization"] = `Token ${userToken}`;

      axios
        .get("http://192.168.0.14:8000/api/auth/user", config)
        .then((res) => {
          dispatch({
            type: "RESTORE_TOKEN",
            token: userToken,
            user: res.data,
          });
        })
        .catch((err) => {
          console.log(err);
          return;
        });
    };

    bootstrapAsync();
  }, []);

  const authContext = React.useMemo(
    () => ({
      signIn: async (email, password) => {
        const config = {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        };

        // Request Body
        const body = JSON.stringify({ email, password });
        axios
          .post("http://192.168.0.14:8000/api/auth/login", body, config)
          .then((res) => {
            SecureStore.setItemAsync("userToken", res.data.token);
            dispatch({
              type: "SIGN_IN",
              token: res.data.token,
              user: res.data.user,
            });
          })
          .catch((err) => {
            console.log(err);
            return;
          });
      },
      signOut: () => {
        SecureStore.deleteItemAsync("userToken");
        dispatch({ type: "SIGN_OUT" });
      },
      updateDetails: async (state, data) => {
        const config = {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        };

        config.headers["Authorization"] = `Token ${state.userToken}`;

        axios
          .put(
            `http://192.168.0.14:8000/api/user/${state.user.id}/`,
            data,
            config
          )
          .then((res) => {
            dispatch({
              type: "UPDATE_USER",
              user: res.data,
            });
          })
          .catch((err) => {
            console.log(err);
            return;
          });
      },
      signUp: async (data) => {
        const config = {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        };

        axios
          .post("http://192.168.0.14:8000/api/auth/register", data, config)
          .then((res) => {
            SecureStore.setItemAsync("userToken", res.data.token);
            dispatch({
              type: "SIGN_IN",
              token: res.data.token,
              user: res.data.user,
            });
          })
          .catch((err) => {
            console.log(err);
            return;
          });
      },
    }),
    []
  );

  return (
    <AuthContext.Provider value={authContext}>
      <AuthState.Provider value={state}>
        <AuthDispatch.Provider value={dispatch}>
          {children}
        </AuthDispatch.Provider>
      </AuthState.Provider>
    </AuthContext.Provider>
  );
};
