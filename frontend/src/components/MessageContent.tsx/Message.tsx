import React, { useEffect, useRef } from "react";
import "./Message.css";
import ReactMarkdown from "react-markdown";

export interface Message {
  user: string;
  type: string;
  content: string;
}

export default function Messages({
  messages,
  searching,
}: {
  messages: Message[];
  searching: boolean;
}) {
  const scrollRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    if (!scrollRef.current) return;
    scrollRef.current.scroll({
      behavior: "smooth",
      top: scrollRef.current.scrollHeight,
    });
  }, [messages, searching]);

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
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        );
      })}
      {searching ? <div className="message-ia-normal">...</div> : null}
    </div>
  );
}
