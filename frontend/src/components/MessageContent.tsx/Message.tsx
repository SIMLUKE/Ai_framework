import React from "react";
import "./Message.css";

export interface Message {
  user: string;
  type: string;
  content: string;
}

export default function Messages({ messages }: { messages: Message[] }) {
  return (
    <div className="message-container">
      {messages.map((message) => {
        return (
          <div
            className={
              message.user === "ia"
                ? "message-" + message.type
                : "message-normal"
            }
          >
            {message.content}
          </div>
        );
      })}
    </div>
  );
}
