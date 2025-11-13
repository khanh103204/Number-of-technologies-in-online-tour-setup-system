<template>
  <nav class="navbar">
    <div class="container">
      <!-- Logo -->
      <div class="logo">
        <img src="/logo.jpg" alt="Logo" />
        <h1>TravelNow</h1>
      </div>

      <!-- Menu chính -->
      <ul class="nav-links">
        <li><RouterLink to="/tours">Tour</RouterLink></li>
        <li><RouterLink to="/recommend">Gợi ý AI</RouterLink></li>
        <li><RouterLink to="/booking">Booking</RouterLink></li>
        <li><RouterLink to="/payment">Thanh toán</RouterLink></li>

        <!-- ✅ Mục mới: Tour của tôi -->
        <li v-if="user">
          <RouterLink to="/my-bookings">Tour của tôi</RouterLink>
        </li>

        <!-- ✅ Chỉ hiện nếu là admin -->
        <li v-if="user && user.role === 'admin'">
          <RouterLink to="/admin" class="btn btn-admin">Quản lý Tour</RouterLink>
        </li>
      </ul>

      <!-- Auth buttons -->
      <div class="auth-buttons">
        <template v-if="!user">
          <RouterLink to="/login" class="btn btn-login">Đăng nhập</RouterLink>
          <RouterLink to="/register" class="btn btn-register">Đăng ký</RouterLink>
        </template>

        <template v-else>
          <span class="welcome">
            👋 Xin chào,
            <b>{{ user.role === 'admin' ? 'Admin' : user.name || 'User' }}</b>
          </span>
          <button class="btn btn-logout" @click="logout">Đăng xuất</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { authStore } from "../stores/auth"; // ✅ đúng đường dẫn

const router = useRouter();

// Tự động đồng bộ user từ store
const user = computed(() => authStore.user);

// Khi load trang, nếu có dữ liệu user trong localStorage thì set lại
onMounted(() => {
  const token = localStorage.getItem("access_token");
  const storedUser = localStorage.getItem("user");
  if (token && storedUser && !authStore.user) {
    try {
      authStore.setUser(JSON.parse(storedUser));
    } catch (err) {
      console.error("Lỗi parse user:", err);
      localStorage.removeItem("user");
    }
  }
});

// Đăng xuất
function logout() {
  authStore.logout();
  router.push("/login");
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 0.8rem 2rem;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo img {
  width: 40px;
  height: 40px;
}

.logo h1 {
  font-size: 20px;
  color: #0f62fe;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 20px;
  list-style: none;
}

.nav-links li {
  display: flex;
  align-items: center;
}

/* Link chung */
.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.3s;
}

.nav-links a:hover {
  color: #0f62fe;
  background: #e6f0ff;
}

/* Nút admin nổi bật */
.btn-admin {
  background: #0f62fe;
  color: white;
  font-weight: 600;
}

.btn-admin:hover {
  background: #0053d6;
  color: white;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn {
  text-decoration: none;
  padding: 6px 14px;
  border-radius: 6px;
  transition: all 0.3s;
  font-weight: 500;
  cursor: pointer;
}

.btn-login {
  border: 1px solid #0f62fe;
  color: #0f62fe;
}

.btn-login:hover {
  background: #0f62fe;
  color: white;
}

.btn-register {
  background: #0f62fe;
  color: white;
}

.btn-register:hover {
  background: #0053d6;
}

.btn-logout {
  background: #ff4d4d;
  color: white;
  border: none;
}

.btn-logout:hover {
  background: #e60000;
}

.welcome {
  font-weight: 500;
  color: #333;
}
</style>
