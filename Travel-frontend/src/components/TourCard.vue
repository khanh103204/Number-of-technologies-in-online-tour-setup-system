<template>
  <div class="tour-card" @click="goToDetail">
    <img :src="imageUrl" :alt="tour.title" class="tour-image" />
    <div class="tour-content">
      <h3 class="tour-title">{{ tour.title }}</h3>
      <p class="tour-location">📍 {{ tour.location }}</p>
      <p class="tour-price">💰 {{ formattedPrice }}</p>
      <p class="tour-description">
        {{ tour.description ? truncate(tour.description) : "Chưa có mô tả chi tiết." }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

interface Tour {
  id: number;
  title: string;
  location: string;
  price: number;
  image: string;
  description?: string;
}

const props = defineProps<{ tour: Tour }>();
const API_BASE = "http://localhost:8000";

// ✅ Tạo link ảnh hợp lệ
const imageUrl = computed(() => {
  if (!props.tour.image) return "/images/default-tour.jpg";
  return props.tour.image.startsWith("http")
    ? props.tour.image
    : `${API_BASE}${props.tour.image.startsWith("/") ? "" : "/"}${props.tour.image}`;
});

// ✅ Định dạng giá tiền đúng chuẩn Việt Nam
const formattedPrice = computed(() => {
  if (!props.tour.price) return "Liên hệ";
  return props.tour.price.toLocaleString("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0,
  });
});

function truncate(text: string, length = 80) {
  return text.length > length ? text.substring(0, length) + "..." : text;
}

function goToDetail() {
  router.push({ name: "TourDetail", params: { id: props.tour.id } });
}
</script>

<style scoped>
.tour-card {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
}
.tour-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.15);
}

.tour-image {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.tour-content {
  padding: 1rem 1.2rem;
}

.tour-title {
  font-size: 1.2rem;
  color: #1a237e;
  margin-bottom: 0.4rem;
}

.tour-location {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 0.3rem;
}

.tour-price {
  color: #ff6b00;
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.6rem;
}

.tour-description {
  color: #444;
  font-size: 0.95rem;
  line-height: 1.5;
}
</style>
