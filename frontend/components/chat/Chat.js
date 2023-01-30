import React, { useState, useCallback, useEffect } from "react";
import { GiftedChat } from "react-native-gifted-chat";
import { API_URLL as API_URL } from "@env";
import { useAuthState } from "../../context/AuthContext";
import useWebSocket, { ReadyState } from "react-native-use-websocket";

export function Chat({ toUser }) {
  const [messages, setMessages] = useState([]);

  const authState = useAuthState();
  const userIds = [authState.user.id, toUser.id].sort();
  const roomName = `${userIds[0]}__${userIds[1]}`;
  const { readyState } = useWebSocket(
    `ws://137.195.118.52:8000/ws/chat/${roomName}/`,
    {
      onMessage: (e) => {
        if (typeof e.data === "string") {
          let data = JSON.parse(e.data);
          setMessages((previousMessages) =>
            GiftedChat.append(previousMessages, data.message)
          );
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
    `ws://137.195.118.52:8000/ws/chat/${roomName}/`
  );

  useEffect(() => {
    setMessages([]);

    // client.onerror = function (e) {
    //   console.log("Connection Error: " + JSON.stringify(e));
    //   console.log("Connection Error");
    // };

    // client.onopen = function () {
    //   console.log("WebSocket Client Connected");
    // };

    // client.onclose = function () {
    //   console.log("echo-protocol Client Closed");
    // };

    // client.onmessage = function (e) {
    //   if (typeof e.data === "string") {
    //     let data = JSON.parse(e.data);

    //     console.log(data);

    //     setMessages((previousMessages) =>
    //       GiftedChat.append(previousMessages, data.message)
    //     );
    //   }
    // };
    return () => {};
  }, []);

  const onSend = useCallback((messages = []) => {
    console.log("Sending Message");
    console.log(messages);
    sendJsonMessage({
      type: "chat_message",
      message: messages,
    });
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
