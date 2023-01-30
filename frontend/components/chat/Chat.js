export function Chat({ toUser }) {
  return (
    // <GiftedChat
    //     messages={messages}
    //     onSend={(messages) => onSend(messages)}
    //     user={{
    //       _id: authState.user.id,
    //     }}
    //   />
    <ScrollView>
      {messageHistory.map((message) => (
        <Text>{message.content}</Text>
      ))}
    </ScrollView>
  );
}
