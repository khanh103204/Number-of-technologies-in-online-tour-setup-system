<template>
  <div class="tour-detail" v-if="tour">
    <div class="image-section">
      <img :src="tour.image" :alt="tour.title" class="tour-image" />
    </div>

    <div class="info-section">
      <h1>{{ tour.title }}</h1>
      <p class="location">📍 {{ tour.location }}</p>
      <p class="price">💰 {{ formattedPrice }}</p>
      <p class="description">{{ tour.description || "Chưa có mô tả chi tiết." }}</p>

      <button class="book-btn" @click="goToBooking">Đặt tour ngay</button>
    </div>
  </div>

  <div v-else class="loading">
    Đang tải dữ liệu tour...
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../api/axios";

const API_BASE = "http://localhost:8000";

interface Tour {
  id: number;
  title: string;
  location: string;
  price: number;
  image: string;
  description?: string;
}

const route = useRoute();
const router = useRouter();
const tour = ref<Tour | null>(null);

// ✅ Định dạng giá tiền theo chuẩn Việt Nam
const formattedPrice = computed(() => {
  if (!tour.value) return "";
  return tour.value.price.toLocaleString("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0,
  });
});

async function fetchTourDetail() {
  const id = route.params.id;
  if (!id) return;

  try {
    const res = await api.get(`/tours/${id}`);
    const data = res.data;

    // Nếu backend trả về chi tiết tour
    if (data) {
      tour.value = {
        id: data.id,
        title: data.name || data.title || "Tour chưa có tên",
        location: data.location || "Đang cập nhật",
        price: data.price || 0,
        image: data.image
          ? data.image.startsWith("http")
            ? data.image
            : `${API_BASE}${data.image.startsWith("/") ? "" : "/"}${data.image}`
          : "/images/default-tour.jpg",
        description: data.description || "",
      };
    }
  } catch (err) {
    console.error("❌ Lỗi tải chi tiết tour:", err);
    alert("Không thể tải thông tin tour. Vui lòng thử lại!");
  }
}

function goToBooking() {
  if (!tour.value) return;
  router.push({
    name: "Booking",
    query: { tour_id: tour.value.id, name: tour.value.title, price: tour.value.price },
  });
}

onMounted(() => {
  fetchTourDetail();
});
</script>

<style scoped>
.tour-detail {
  max-width: 900px;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  font-family: "Segoe UI", Arial, sans-serif;
}

.image-section {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
}

.tour-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.15);
}

.info-section h1 {
  font-size: 2rem;
  color: #1a237e;
  margin-bottom: 0.5rem;
}

.location {
  color: #666;
  margin-bottom: 0.5rem;
}

.price {
  color: #ff6b00;
  font-weight: bold;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.description {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.book-btn {
  padding: 0.8rem 1.4rem;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}
.book-btn:hover {
  background-color: #125ea5;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #555;
  margin-top: 2rem;
}
</style>
