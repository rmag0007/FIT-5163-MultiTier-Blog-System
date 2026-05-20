import axios from "axios";

const client = axios.create({
  baseURL: "https://localhost:5000/api",
});

// Automatically attach JWT to every request
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default client;