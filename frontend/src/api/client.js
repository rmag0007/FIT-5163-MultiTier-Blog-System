import axios from "axios";

const client = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  // Required because we use a self-signed cert in development
  httpsAgent: undefined
});

// Automatically attach JWT token to every request if it exists
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Automatically handle 401 responses — token expired or invalid
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("tier");
      localStorage.removeItem("username");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default client;