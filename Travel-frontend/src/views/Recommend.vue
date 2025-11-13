<template>
  <div class="recommend-page">
    <div class="background-overlay"></div>

    <div class="container">
      <!-- Form gợi ý tour -->
      <div class="recommend-card">
        <h2>✨ Gợi ý tour thông minh từ AI</h2>
        <p>
          Hãy nhập yêu cầu tour bằng câu tự nhiên, ví dụ:
          <em>"Tôi muốn tour biển Nha Trang cho 4 người, 2 ngày 1 đêm, giá dưới 5 triệu"</em>
        </p>

        <form @submit.prevent="doRecommend" class="recommend-form">
          <div class="form-group">
            <label>Nhập yêu cầu tour</label>
            <input v-model="query" type="text" placeholder="Nhập câu tự nhiên..." />
          </div>

          <div class="form-group">
            <label>Số lượng tour muốn gợi ý</label>
            <input v-model.number="topN" type="number" min="1" max="20" />
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? "⏳ Đang tìm..." : "🚀 Lấy gợi ý" }}
          </button>
        </form>
      </div>

      <!-- Tiêu chí AI hiểu -->
      <div v-if="criteria && Object.keys(criteria).length" class="criteria-box">
        <h4>🤖 AI hiểu bạn muốn:</h4>
        <ul>
          <li v-for="(val, key) in criteria" :key="key">
            {{ key }}: <strong>{{ val }}</strong>
          </li>
        </ul>
      </div>

      <!-- Danh sách tour -->
      <div v-if="tours.length" class="tour-list">
        <div v-for="tour in tours" :key="tour.tour_id" class="tour-card">
          <img
            :src="getTourImage(tour.type)"
            alt="Tour"
            class="tour-image"
            @click="goToDetail(tour.tour_id)"
          />

          <div class="tour-info">
            <h3>{{ tour.tour_name }}</h3>
            <p><strong>🆔 ID:</strong> {{ tour.tour_id }}</p>
            <p><strong>📍 Địa điểm:</strong> {{ tour.location }}</p>
            <p><strong>🏷 Loại hình:</strong> {{ tour.type }}</p>
            <p><strong>💰 Giá:</strong> {{ formatPrice(tour.price) }}</p>
            <p><strong>🕒 Thời lượng:</strong> {{ tour.duration_days }} ngày</p>
            <p><strong>⭐ Đánh giá:</strong> {{ tour.rating_avg }}/5</p>

            <div v-if="tour.similar && tour.similar.length" class="similar-box">
              <h4>🎯 Các tour tương tự:</h4>
              <ul>
                <li v-for="sim in tour.similar" :key="sim.tour_id">
                  {{ sim.tour_name }} — độ tương đồng:
                  <strong>{{ sim.similarity?.toFixed(2) || "0.00" }}</strong>
                </li>
              </ul>
            </div>

            <!-- 🛒 Nút đặt tour -->
            <button class="book-btn" @click="bookTour(tour)">
              🛒 Đặt tour
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="toursLoaded && !loading" class="no-tour">
        😢 Không tìm thấy tour phù hợp với yêu cầu.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api/axios";

const router = useRouter();
const query = ref("");
const topN = ref(5);
const tours = ref<any[]>([]);
const toursLoaded = ref(false);
const loading = ref(false);
const criteria = ref<any | null>(null);

// 👉 Xem chi tiết tour
function goToDetail(tourId: number) {
  router.push({ name: "TourDetail", params: { id: tourId } });
}

// 👉 Đặt tour
function bookTour(tour: any) {
  if (!tour?.tour_id) {
    alert("❌ Không thể đặt tour: thiếu ID hợp lệ!");
    return;
  }
  localStorage.setItem("selectedTour", JSON.stringify(tour));
  router.push({ name: "Booking" });
}

function getTourImage(type: string) {
  const t = (type || "").toLowerCase();
  if (t.includes("biển") || t.includes("đảo"))
    return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80";
  if (t.includes("núi") || t.includes("leo"))
    return "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=800&q=80";
  if (t.includes("cắm") || t.includes("trại"))
    return "https://images.unsplash.com/photo-1505678261036-a3fcc5e884ee?w=800&q=80";
  if (t.includes("thành phố") || t.includes("city"))
    return "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?w=800&q=80";
  return "https://images.unsplash.com/photo-1519824145371-296894a0daa9?w=800&q=80";
}

function formatPrice(price: number | null | undefined) {
  if (!price || isNaN(price)) return "N/A";
  return price.toLocaleString("vi-VN") + " VND";
}

async function doRecommend() {
  toursLoaded.value = false;
  tours.value = [];
  criteria.value = null;
  loading.value = true;

  try {
    const res = await api.post("/recommend/query", {
      query: query.value,
      top_n: topN.value,
    });

    criteria.value = res.data.criteria || {};

    tours.value =
      res.data.recommendations?.map((tour: any) => ({
        tour_id: tour.tour_id || tour.id,
        tour_name: tour.tour_name || tour.name,
        location: tour.location,
        type: tour.type,
        price: tour.price,
        duration_days: tour.duration_days,
        rating_avg: tour.rating_avg || 4.5,
        similar: tour.similar || [],
      })) || [];
  } catch (err) {
    console.error(err);
    alert("❌ Lỗi khi lấy dữ liệu gợi ý từ server.");
  } finally {
    loading.value = false;
    toursLoaded.value = true;
  }
}
</script>

<style scoped>
/* === Tổng thể trang === */
.recommend-page {
  font-family: "Poppins", sans-serif;
  position: relative;
  padding-bottom: 2rem;
}

.background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1600&q=80")
    center/cover no-repeat;
  filter: brightness(0.65) blur(4px);
  z-index: -1;
}

.container {
  max-width: 1100px;
  margin: 3rem auto;
  padding: 1.5rem;
  z-index: 1;
}

/* === Form gợi ý === */
.recommend-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(6px);
  padding: 1.8rem;
  border-radius: 18px;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.1);
}
.recommend-card h2 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}
.recommend-card p {
  color: #555;
  margin-bottom: 1rem;
}
.recommend-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.form-group {
  display: flex;
  flex-direction: column;
}
.form-group input {
  padding: 0.6rem;
  border-radius: 10px;
  border: 1px solid #bbb;
}
.submit-btn {
  padding: 0.9rem;
  background: linear-gradient(90deg, #1976d2, #42a5f5);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}
.submit-btn:hover {
  background: linear-gradient(90deg, #1565c0, #1e88e5);
}
.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* === Tiêu chí AI === */
.criteria-box {
  margin-top: 1.2rem;
  background: rgba(255, 255, 255, 0.85);
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.criteria-box h4 {
  color: #1565c0;
  margin-bottom: 0.4rem;
}

/* === Danh sách tour === */
.tour-list {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1.5rem;
}

.tour-card {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}
.tour-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}
.tour-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  cursor: pointer;
}
.tour-info {
  padding: 1rem;
}
.tour-info h3 {
  font-size: 1.1rem;
  color: #0d47a1;
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.similar-box {
  margin-top: 0.8rem;
  background: #f6f9ff;
  padding: 0.6rem 0.8rem;
  border-radius: 10px;
  font-size: 0.9rem;
}
.book-btn {
  width: 100%;
  margin-top: 0.8rem;
  padding: 0.8rem;
  background: #1e88e5;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  transition: 0.3s;
  cursor: pointer;
}
.book-btn:hover {
  background: #1565c0;
}
.no-tour {
  text-align: center;
  color: #666;
  margin-top: 2rem;
  font-size: 1.1rem;
}
</style>
