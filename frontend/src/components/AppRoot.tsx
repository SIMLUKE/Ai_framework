import React, { useEffect, useMemo, useRef, useState } from "react";
import ChatBox from "./ChatBox/ChatBox";

export default function AppRoot() {
  return (
    <div className="app-container">
      <ChatBox></ChatBox>
    </div>
  );
}
