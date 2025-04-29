import React, { useState } from "react";
import "./ChatBox.css";
import Messages, { Message } from "../MessageContent.tsx/Message";
import UserInput from "../UserInput/UserInput";

export default function ChatBox() {
  const [searching, setSearching] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      user: "ia",
      type: "ia-search",
      content:
        "Hello, welcome to the env smart ai, pls ask only necessary questions",
    },
    //    {
    //      user: "ia",
    //      type: "ia-code",
    //      content: "search message",
    //    },
    //    {
    //      user: "ia",
    //      type: "ia-man_page",
    //      content: "man error",
    //    },
    //    {
    //      user: "ia",
    //      type: "ia-error",
    //      content: "error",
    //    },
    //    {
    //      user: "user",
    //      type: "ia-code",
    //      content: "search message qsfsd ffdsfdsfsf dsf sdfsd fsdf sdf s",
    //    },
  ]);
  return (
    <div className="chat-box">
      <Messages messages={messages} searching={searching}></Messages>
      <UserInput
        setMessages={setMessages}
        searching={searching}
        setSearching={setSearching}
      ></UserInput>
    </div>
  );
}
