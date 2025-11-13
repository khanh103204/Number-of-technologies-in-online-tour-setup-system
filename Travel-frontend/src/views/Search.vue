<template>
  <div class="search-page">
    <div class="search-header">
      <h2>Tìm kiếm Tour du lịch</h2>
      <div class="search-bar">
        <input
          v-model="query"
          type="text"
          placeholder="Nhập tên tour, địa điểm..."
          @keyup.enter="fetchTours"
        />
        <button @click="fetchTours">Tìm kiếm</button>
      </div>
    </div>

    <div class="filter-bar">
      <select v-model="filter.location" @change="fetchTours">
        <option value="">-- Địa điểm --</option>
        <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
      </select>

      <select v-model="filter.duration" @change="fetchTours">
        <option value="">-- Thời gian --</option>
        <option value="1">1 ngày</option>
        <option value="2-3">2-3 ngày</option>
        <option value="4+">4 ngày trở lên</option>
      </select>

      <select v-model="filter.price" @change="fetchTours">
        <option value="">-- Giá --</option>
        <option value="duoi-1000000">Dưới 1.000.000đ</option>
        <option value="1000000-3000000">1.000.000đ - 3.000.000đ</option>
        <option value="tren-3000000">Trên 3.000.000đ</option>
      </select>
    </div>

    <div class="tour-list">
      <div v-if="loading" class="loading">Đang tải dữ liệu...</div>

      <div v-else-if="tours.length === 0" class="no-result">
        Không tìm thấy tour nào phù hợp 😢
      </div>

      <div v-else class="grid">
        <div v-for="tour in tours" :key="tour.id" class="tour-card">
          <img :src="tour.image || defaultImg" alt="Tour" />
          <div class="tour-info">
            <h3>{{ tour.title }}</h3>
            <p class="location">📍 {{ tour.location }}</p>
            <p class="price">💰 {{ formatPrice(tour.price) }}</p>
            <p class="duration">🕒 {{ tour.duration }} ngày</p>
            <button @click="viewDetail(tour.id)">Xem chi tiết</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "../api/axios";
import { useRouter } from "vue-router";

const query = ref("");
const tours = ref<any[]>([]);
const loading = ref(false);
const router = useRouter();
const defaultImg = "/default-tour.jpg"; // ảnh mặc định nếu không có ảnh

const filter = ref({
  location: "",
  duration: "",
  price: "",
});

const locations = ["Đà Nẵng", "Nha Trang", "Đà Lạt", "Phú Quốc", "Sa Pa"];

function formatPrice(price: number) {
  return price.toLocaleString("vi-VN") + "đ";
}

async function fetchTours() {
  loading.value = true;
  try {
    const params: any = {};
    if (query.value) params.search = query.value;
    if (filter.value.location) params.location = filter.value.location;
    if (filter.value.duration) params.duration = filter.value.duration;
    if (filter.value.price) params.price = filter.value.price;

    const res = await api.get("/tours", { params });
    tours.value = res.data || [];
  } catch (error) {
    console.error("❌ Lỗi tải tour:", error);
    tours.value = [];
  } finally {
    loading.value = false;
  }
}

function viewDetail(id: number) {
  router.push(`/tours/${id}`);
}

onMounted(fetchTours);
</script>

<style scoped>
.search-page {
  padding: 2rem;
  background: #f5f7fa;
  min-height: 100vh;
}

.search-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.search-header h2 {
  font-size: 1.8rem;
  color: #2c3e50;
}

.search-bar {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 1rem;
}

.search-bar input {
  width: 60%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
}

.search-bar button {
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
}

.search-bar button:hover {
  background: #145ca8;
}

.filter-bar {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 2rem;
}

.filter-bar select {
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.tour-list .grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.tour-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s;
}

.tour-card:hover {
  transform: translateY(-4px);
}

.tour-card img {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.tour-info {
  padding: 1rem;
}

.tour-info h3 {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 0.3rem;
}

.tour-info p {
  margin: 0.2rem 0;
  font-size: 0.9rem;
  color: #555;
}

.tour-info button {
  margin-top: 0.6rem;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
}

.tour-info button:hover {
  background: #145ca8;
}

.loading,
.no-result {
  text-align: center;
  font-size: 1rem;
  color: #555;
  margin-top: 2rem;
}
</style>
