import React, { useEffect, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import Select from "react-select";
import "./Dictaphone.css";
import languages from "./languages";
import { sendSpeech } from "./dictaphoneService";
import { toast } from "react-toastify";

const Dictaphone = () => {
  const [currentCode, setCurrentCode] = useState<string>("es-ES");
  const [speech, setSpeech] = useState<string>("");
  const {
    finalTranscript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  useEffect(() => {
    setSpeech(finalTranscript);
  }, [finalTranscript]);
  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  const options: any[] = languages.map((item) => {
    return { value: item.code, label: item.name };
  });

  return (
    <div className="dictaphone-container">
      <Select
        onChange={(newValue) => {
          setCurrentCode(newValue.value || "es-ES");
        }}
        options={options}
        value={options.find((item) => item.value === currentCode)}
        className="select"
      />
      <div className="dictaphone-header">
        <p>
          {listening ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 -960 960 960"
              width="24px"
              fill="#000000"
            >
              <path d="M480-400q-50 0-85-35t-35-85v-240q0-50 35-85t85-35q50 0 85 35t35 85v240q0 50-35 85t-85 35Zm0-240Zm-40 520v-123q-104-14-172-93t-68-184h80q0 83 58.5 141.5T480-320q83 0 141.5-58.5T680-520h80q0 105-68 184t-172 93v123h-80Zm40-360q17 0 28.5-11.5T520-520v-240q0-17-11.5-28.5T480-800q-17 0-28.5 11.5T440-760v240q0 17 11.5 28.5T480-480Z" />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 -960 960 960"
              width="24px"
              fill="#000000"
            >
              <path d="m710-362-58-58q14-23 21-48t7-52h80q0 44-13 83.5T710-362ZM480-594Zm112 112-72-72v-206q0-17-11.5-28.5T480-800q-17 0-28.5 11.5T440-760v126l-80-80v-46q0-50 35-85t85-35q50 0 85 35t35 85v240q0 11-2.5 20t-5.5 18ZM440-120v-123q-104-14-172-93t-68-184h80q0 83 57.5 141.5T480-320q34 0 64.5-10.5T600-360l57 57q-29 23-63.5 39T520-243v123h-80Zm352 64L56-792l56-56 736 736-56 56Z" />
            </svg>
          )}
        </p>
        <button
          onClick={() =>
            SpeechRecognition.startListening({
              continuous: true,
              language: currentCode,
            })
          }
        >
          Start
        </button>
        <button
          className="stop-button"
          onClick={() => SpeechRecognition.stopListening()}
        >
          Stop
        </button>
        <button onClick={resetTranscript}>Reset</button>
      </div>
      <textarea
        value={speech}
        onChange={(e) => {
          setSpeech(e.target.value);
        }}
      />
      <button
        onClick={() => {
          toast.promise(
            sendSpeech(
              options.find((item) => item.value === currentCode).label,
              speech,
            ),
            {
              pending: "Sending translated speech to customer",
              success: "speech send successfuly",
              error: "An error occured",
            },
          );
        }}
      >
        send
      </button>
    </div>
  );
};
export default Dictaphone;
