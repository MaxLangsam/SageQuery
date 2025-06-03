import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function sendQuery(question, preview = false) {
  const res = await axios.post(`${API_URL}/query/`, { question, preview });
  return res.data;
}

export async function sendFeedback({ question, sql, feedback, correct }) {
  await axios.post(`${API_URL}/feedback/`, { question, sql, feedback, correct });
} 