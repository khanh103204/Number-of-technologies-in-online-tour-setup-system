<template>
  <div class="register-page">
    <!-- 🌅 Background -->
    <div class="background"></div>

    <!-- 🧭 Form đăng ký -->
    <div class="register-container">
      <div class="register-card">
        <h2>🌍 Tạo tài khoản du lịch</h2>
        <p class="subtitle">Tham gia hành trình khám phá thế giới cùng chúng tôi ✈️</p>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="name">👤 Họ và tên</label>
            <input
              id="name"
              v-model="name"
              type="text"
              placeholder="Nhập họ và tên của bạn"
              required
            />
          </div>

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
              placeholder="Tạo mật khẩu an toàn"
              required
            />
          </div>

          <button type="submit" class="register-btn" :disabled="loading">
            {{ loading ? "⏳ Đang xử lý..." : "🚀 Đăng ký ngay" }}
          </button>
        </form>

        <div class="note">
          <p>Đã có tài khoản? <a href="/login">Đăng nhập</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import api from "../api/axios";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const loading = ref(false);
const router = useRouter();

async function handleRegister() {
  if (!name.value || !email.value || !password.value) {
    alert("⚠️ Vui lòng nhập đầy đủ thông tin!");
    return;
  }

  loading.value = true;

  try {
    await api.post("/auth/register", {
      name: name.value,
      email: email.value,
      password: password.value,
      role: "user", // giữ nguyên logic gốc
    });

    alert("✅ Đăng ký thành công! Vui lòng đăng nhập.");
    router.push("/login");
  } catch (e: any) {
    console.error("❌ Lỗi đăng ký:", e);
    const msg =
      e.response?.data?.detail ||
      e.response?.data?.message ||
      "Đăng ký thất bại. Vui lòng thử lại!";
    alert(msg);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* 🌴 Tổng thể */
.register-page {
  position: relative;
  min-height: 100vh;
  font-family: "Poppins", sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 🌅 Hình nền */
.background {
  position: absolute;
  inset: 0;
  background: url("https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=1600&q=80")
    center/cover no-repeat;
  filter: brightness(0.65) blur(3px);
  z-index: -1;
}

/* 📦 Khung chính */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 2rem;
}

.register-card {
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
.register-card h2 {
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
.register-form {
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

/* 🚀 Nút đăng ký */
.register-btn {
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
.register-btn:hover {
  background: linear-gradient(90deg, #1565c0, #2196f3);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(25, 118, 210, 0.3);
}
.register-btn:disabled {
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
