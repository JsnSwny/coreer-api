import React, { useState, useCallback, useEffect } from "react";
import { GiftedChat } from "react-native-gifted-chat";
import { API_URL } from "@env";
import { useAuthState } from "../../context/AuthContext";

export function Chat() {
  const [messages, setMessages] = useState([]);
  const [count, setCount] = useState(0);

  const authState = useAuthState();
  let W3CWebSocket = require("websocket").w3cwebsocket;
  var client = new W3CWebSocket("ws://192.168.0.14:8000/ws/chat/Hello/");

  useEffect(() => {
    setMessages([]);

    client.onerror = function (e) {
      console.log("Connection Error: " + JSON.stringify(e));
      console.log("Connection Error");
    };

    client.onopen = function () {
      console.log("WebSocket Client Connected");
    };

    client.onclose = function () {
      console.log("echo-protocol Client Closed");
    };

    client.onmessage = function (e) {
      if (typeof e.data === "string") {
        let data = JSON.parse(e.data);

        console.log(data);

        setMessages((previousMessages) =>
          GiftedChat.append(previousMessages, data.message)
        );
      }
    };
    return () => {};
  }, []);

  const onSend = useCallback((messages = []) => {
    client.send(
      JSON.stringify({
        message: messages,
      })
    );
  }, []);

  return (
    <GiftedChat
      messages={messages}
      onSend={(messages) => onSend(messages)}
      user={{
        _id: authState.user.id,
      }}
    />
  );
}
