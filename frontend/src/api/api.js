import axios from "axios";

export const API = axios.create({
  baseURL: import.meta.env?.VITE_BACKEND_URL || import.meta.env?.BACKEND_URL || "https://interleet-backend.sharexpress.in",
  withCredentials: true,
});
