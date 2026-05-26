import axios from "axios";

// Axios client used by the frontend to communicate with the Flask API.
// `baseURL` points to the backend dev server; in production this should
// be replaced with the deployed API URL.
const client = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  // `httpsAgent` may be configured to trust self-signed certs in dev.
  httpsAgent: undefined
});

// Attach JWT token from localStorage to every outgoing request when present.
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Global response handler: when the API returns 401 remove local auth
// state and redirect to login so the user can re-authenticate.
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