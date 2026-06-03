import axios from "axios";

export const API = axios.create({
  baseURL: import.meta.env?.BACKEND_URL || "http://localhost:8000",
  withCredentials: true,
});
