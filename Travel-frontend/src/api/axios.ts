// src/api/axios.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // 🔧 Nếu backend dùng /api prefix => đổi thành http://127.0.0.1:8000/api
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ Tự động gắn token vào mọi request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token"); // key đồng nhất với Login.vue
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ✅ Xử lý lỗi token hết hạn (401)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("Token hết hạn hoặc không hợp lệ → đăng xuất...");
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
