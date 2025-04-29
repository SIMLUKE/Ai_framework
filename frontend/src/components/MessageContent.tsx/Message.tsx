import React, { useEffect, useRef } from "react";
import "./Message.css";

export interface Message {
  user: string;
  type: string;
  content: string;
}

export default function Messages({ messages }: { messages: Message[] }) {
  const scrollRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    if (!scrollRef.current) return;
    scrollRef.current.scroll({
      behavior: "smooth",
      top: scrollRef.current.scrollHeight,
    });
  }, [messages]);

  return (
    <div ref={scrollRef} className="message-container">
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
