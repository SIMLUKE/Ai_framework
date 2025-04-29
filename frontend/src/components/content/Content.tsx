import React, { useEffect, useRef } from "react";
import "./Content.css";

interface ContentProps {
  messages: string[];
}

export default function Content({ messages }: ContentProps) {
  const scrollRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    if (!scrollRef.current) return;
    scrollRef.current.scroll({
      behavior: "smooth",
      top: scrollRef.current.scrollHeight,
    });
  }, [messages]);

  return (
    <div ref={scrollRef} className="Content_container">
      {messages.map((message) => (
        <div className="Ia_message">{message}</div>
      ))}
    </div>
  );
}
