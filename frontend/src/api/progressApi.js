import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getProgress = (userId) => {
  return API.get(`/progress/${userId}`);
};