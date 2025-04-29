import axios from "axios";

export default async function sendPrompt(prompt: String) {
  return await axios
    .post(`http://0.0.0.0:8080/prompt`, {
      input: prompt,
    })
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      throw err;
    });
}
