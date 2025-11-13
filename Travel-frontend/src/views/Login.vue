<template>
  <div class="login-page">
    <!-- Hình nền du lịch -->
    <div class="background"></div>

    <!-- Form đăng nhập -->
    <div class="login-container">
      <div class="login-card">
        <h2>🌍 Đăng nhập hệ thống du lịch</h2>
        <p class="subtitle">Khám phá thế giới cùng chúng tôi ✈️</p>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">📧 Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="Nhập email của bạn"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">🔒 Mật khẩu</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Nhập mật khẩu"
              required
            />
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            {{ loading ? "⏳ Đang đăng nhập..." : "🚀 Đăng nhập" }}
          </button>
        </form>

        <div class="note">
          <p>Chưa có tài khoản? <a href="/register">Đăng ký ngay</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import api from "../api/axios";
import { useRouter } from "vue-router";
import { authStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const loading = ref(false);
const router = useRouter();

function decodeJwt(token: string) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const json = atob(base64);
    try {
      return JSON.parse(decodeURIComponent(escape(json)));
    } catch {
      return JSON.parse(json);
    }
  } catch {
    return null;
  }
}

async function handleLogin() {
  if (!email.value || !password.value) {
    alert("⚠️ Vui lòng nhập đầy đủ thông tin!");
    return;
  }

  loading.value = true;

  try {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    const form = new URLSearchParams();
    form.append("username", email.value);
    form.append("password", password.value);

    const res = await api.post("/auth/token", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const token = res.data?.access_token;
    if (!token) throw new Error("Không nhận được access_token từ server");

    localStorage.setItem("access_token", token);

    const payload = decodeJwt(token);
    const roleFromToken = payload?.role || "user";

    const me = await api.get("/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const role = (me.data.role || roleFromToken).toLowerCase();
    const name = me.data.name || me.data.email?.split("@")[0] || "Người dùng";

    const userData = { ...me.data, role, name };
    localStorage.setItem("user", JSON.stringify(userData));

    authStore.setUser(userData);

    alert(`✅ Đăng nhập thành công! Xin chào ${userData.name}`);

    router.replace(role === "admin" ? "/admin" : "/tours");
  } catch (err: any) {
    console.error("❌ Lỗi đăng nhập:", err);
    const msg =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      err.message ||
      "Đăng nhập thất bại. Vui lòng thử lại!";
    alert(msg);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* 🌴 Tổng thể */
.login-page {
  position: relative;
  min-height: 100vh;
  font-family: "Poppins", sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 🌊 Hình nền du lịch */
.background {
  position: absolute;
  inset: 0;
  background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80")
    center/cover no-repeat;
  filter: brightness(0.6) blur(3px);
  z-index: -1;
}

/* 📦 Khung chính */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 2rem;
}

.login-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem 2.5rem;
  border-radius: 20px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
  max-width: 420px;
  width: 100%;
  text-align: center;
  animation: fadeIn 0.8s ease;
}

/* 🎨 Tiêu đề */
.login-card h2 {
  color: #1976d2;
  font-weight: 700;
  margin-bottom: 0.3rem;
}
.subtitle {
  color: #555;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

/* 🧾 Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  text-align: left;
}

.form-group label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.3rem;
  display: block;
}

.form-group input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #bbb;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  border-color: #1976d2;
  box-shadow: 0 0 6px rgba(25, 118, 210, 0.3);
  outline: none;
}

/* 🚀 Nút đăng nhập */
.login-btn {
  background: linear-gradient(90deg, #1976d2, #42a5f5);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  font-size: 1rem;
}
.login-btn:hover {
  background: linear-gradient(90deg, #1565c0, #2196f3);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(25, 118, 210, 0.3);
}
.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 🧭 Ghi chú */
.note {
  margin-top: 1.2rem;
  color: #444;
  font-size: 0.9rem;
}
.note a {
  color: #1976d2;
  font-weight: bold;
  text-decoration: none;
}
.note a:hover {
  text-decoration: underline;
}

/* ✨ Hiệu ứng */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
