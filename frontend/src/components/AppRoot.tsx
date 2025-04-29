import React, { useEffect, useMemo, useRef, useState } from "react";
import Content from "./content/Content";
import "../routes/App/App.css";
import { Bounce, toast } from "react-toastify";
import Select from "react-select";

const options: any[] = [
  { value: "EN", label: "English" },
  { value: "FR", label: "French" },
  { value: "CH", label: "Chinese" },
  { value: "ES", label: "Spanish" },
];

export default function AppRoot() {
  const [translatedMessage, setTranslatedMessage] = useState<string[]>([]);
  const [listening, setListening] = useState<boolean>(false);
  const [currentCountry, setCurrentCountry] = useState<string>("EN");

  const webSocketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    webSocketRef.current = new WebSocket(
      `ws://0.0.0.0:8080/message/${currentCountry}`,
    );
    return () => {
      webSocketRef.current?.close();
    };
  }, [currentCountry]);

  useEffect(() => {
    if (webSocketRef.current == null) {
      return;
    } else {
      webSocketRef.current.onmessage = (ev) => {
        try {
          const message = JSON.parse(ev.data as string);
          if (message.start) {
            setTranslatedMessage((previous) => {
              const toReturn = [...previous];
              toReturn.push(message.data || "");
              return toReturn;
            });
          } else {
            setTranslatedMessage((previous) => {
              const toReturn = [...previous];
              if (toReturn.length === 0) {
                toReturn.push("");
              }
              toReturn[toReturn.length - 1] += message.data || "";
              return toReturn;
            });
          }
          if (message.end) {
            setListening(false);
          }
        } catch {
          toast.error("Error listening to translation", {
            position: "top-center",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: false,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "colored",
            transition: Bounce,
          });
        }
      };
    }
  }, [webSocketRef, listening, setTranslatedMessage, currentCountry]);

  return (
    <div className="app-container">
      <div className="select-container">
        <Select
          onChange={(newValue) => {
            setCurrentCountry(newValue.value || "EN");
          }}
          options={options}
          value={options.find((item) => item.value === currentCountry)}
          className="select"
        />
      </div>
      <Content messages={translatedMessage} />
    </div>
  );
}
