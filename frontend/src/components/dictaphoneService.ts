import axios from "axios";

export async function sendSpeech(language: string, speech: string) {
  axios
    .post("http://0.0.0.0:8080/prompt", {
      baseLanguage: language,
      text: speech,
    })
    .catch((e) => {
      throw e;
    });
}
