<template>
  <div class="my-bookings">
    <h1>🧳 Các tour đã đặt</h1>

    <div v-if="loading" class="loading">Đang tải dữ liệu...</div>

    <div v-else-if="bookings.length" class="booking-list">
      <div v-for="(b, i) in bookings" :key="i" class="booking-card">
        <div class="booking-info">
          <h2>{{ b.tour?.name || "Chưa có tên tour" }}</h2>
          <p>📍 {{ b.tour?.location || "Không rõ địa điểm" }}</p>
          <p>👥 Số người: {{ b.number_people }}</p>
          <p>🗓️ Ngày đặt: {{ formatDate(b.created_at) }}</p>
          <p class="price">💰 {{ formatPrice(b.total_price) }}</p>

          <p class="status" :class="b.status === 'paid' ? 'paid' : 'pending'">
            {{ b.status === 'paid' ? '✅ Đã thanh toán' : '⏳ Chờ thanh toán' }}
          </p>

          <router-link
            v-if="b.tour?.id"
            :to="`/tours/${b.tour.id}`"
            class="btn-detail"
          >
            Xem chi tiết
          </router-link>
        </div>
      </div>
    </div>

    <div v-else class="no-bookings">
      <p>Bạn chưa đặt tour nào 😅</p>
      <router-link to="/tours" class="btn-go">Đặt tour ngay</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

interface Booking {
  id: number;
  number_people: number;
  total_price: number;
  status: string;
  created_at: string;
  tour: {
    id: number;
    name: string; // ✅ backend trả về "name", không phải "title"
    location: string;
    price: number;
  };
}

const bookings = ref<Booking[]>([]);
const loading = ref(true);

onMounted(async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Vui lòng đăng nhập để xem danh sách đặt tour!");
    window.location.href = "/login";
    return;
  }

  try {
    const res = await axios.get("http://localhost:8000/bookings/me", {
      headers: { Authorization: `Bearer ${token}` },
    });
    bookings.value = res.data;
  } catch (err: any) {
    console.error("❌ Lỗi tải danh sách đặt tour:", err);
    if (err.response?.status === 401) {
      alert("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!");
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    } else {
      alert("Không thể tải danh sách đặt tour. Vui lòng thử lại!");
    }
  } finally {
    loading.value = false;
  }
});

const formatPrice = (v: number) => v.toLocaleString("vi-VN") + " ₫";
const formatDate = (d: string) =>
  new Date(d).toLocaleDateString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
</script>

<style scoped>
.my-bookings {
  padding: 40px 80px;
  background: #f9fafc;
  min-height: 100vh;
}
.my-bookings h1 {
  font-size: 28px;
  margin-bottom: 30px;
  color: #0f62fe;
  text-align: center;
}
.loading {
  text-align: center;
  color: #888;
  font-size: 18px;
  margin-top: 50px;
}
.booking-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.booking-card {
  display: flex;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  transition: transform 0.2s;
}
.booking-card:hover {
  transform: translateY(-3px);
}
.booking-info {
  flex: 1;
}
.booking-info h2 {
  font-size: 20px;
  color: #111;
  margin-bottom: 8px;
}
.price {
  color: #ff6b00;
  font-weight: bold;
  margin: 6px 0;
}
.status {
  font-weight: 600;
  margin: 6px 0;
}
.status.paid {
  color: green;
}
.status.pending {
  color: orange;
}
.btn-detail,
.btn-go {
  display: inline-block;
  background: #0f62fe;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-detail:hover,
.btn-go:hover {
  background: #0043ce;
}
.no-bookings {
  text-align: center;
  margin-top: 80px;
}
</style>
