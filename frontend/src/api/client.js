import axios from "axios";

const apiBase = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: apiBase,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function getHealth() {
  const { data } = await apiClient.get("/api/health/");
  return data;
}

export default apiClient;
