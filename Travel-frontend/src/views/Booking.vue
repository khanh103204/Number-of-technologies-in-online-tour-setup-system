<template>
  <div class="booking-page">
    <!-- Background mờ -->
    <div class="background-overlay"></div>

    <div class="container">
      <div class="booking-container">
        <!-- Cột trái -->
        <div class="left-column">
          <!-- Slogan -->
          <div class="slogan">
            <h2>Khám phá Việt Nam cùng TravelNow</h2>
            <p>✈️ Hành trình tuyệt vời bắt đầu từ đây!</p>
          </div>

          <!-- Form đặt tour -->
          <form @submit.prevent="doBooking" class="booking-form">
            <div class="form-group">
              <label for="tourId">ID tour</label>
              <input
                id="tourId"
                v-model.number="tour_id"
                type="number"
                min="1"
                placeholder="Nhập ID tour"
              />
            </div>

            <div class="form-group">
              <label for="numberPeople">Số người</label>
              <input
                id="numberPeople"
                v-model.number="number_people"
                type="number"
                min="1"
                placeholder="Nhập số người"
              />
            </div>

            <button type="submit" class="submit-btn">Đặt ngay</button>
          </form>

          <!-- Tips -->
          <div class="tips">
            <h3>💡 Tips đặt tour</h3>
            <ul>
              <li>Đặt tour sớm để đảm bảo chỗ.</li>
              <li>Kiểm tra chính sách hủy trước khi đặt.</li>
              <li>Chọn tour phù hợp số người và sở thích.</li>
              <li>Mang theo giấy tờ tùy thân khi đi tour.</li>
            </ul>
          </div>

          <!-- Thống kê -->
          <div class="stats">
            <div class="stat-card">
              <h4>{{ totalBookings }}</h4>
              <p>Tour đã đặt hôm nay</p>
            </div>
            <div class="stat-card">
              <h4>{{ totalVisitors }}</h4>
              <p>Khách đang đặt tour</p>
            </div>
            <div class="stat-card">
              <h4>10</h4>
              <p>Top tour phổ biến</p>
            </div>
          </div>

          <!-- Thông tin booking -->
          <div v-if="booking" class="booking-info">
            <h3>🎉 Booking thành công!</h3>
            <p><strong>ID booking:</strong> {{ booking.id }}</p>
            <p><strong>Tên tour:</strong> {{ booking.tour.name }}</p>
            <p><strong>Địa điểm:</strong> {{ booking.tour.location || "Đang cập nhật" }}</p>
            <p><strong>Số người:</strong> {{ booking.number_people }}</p>
            <p><strong>Tổng tiền:</strong> {{ formattedTotalPrice }}</p>
            <p><strong>Trạng thái:</strong> {{ booking.status }}</p>
            <p><strong>Ngày tạo:</strong> {{ booking.created_at }}</p>

            <button class="pay-btn" @click="goToPayment">
              💳 Thanh toán ngay
            </button>
          </div>

          <!-- CTA -->
          <div class="cta">
            <button class="view-tours-btn" @click="goToTours">🔍 Xem tất cả tour</button>
          </div>
        </div>

        <!-- Cột phải -->
        <div class="right-column">
          <h3>🌏 Thông tin du lịch Việt Nam</h3>
          <div class="info-cards">
            <div
              v-for="(card, index) in travelCards"
              :key="index"
              ref="cards"
              class="info-card"
            >
              <h4>{{ card.title }}</h4>
              <p>{{ card.content }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api/axios";

interface Tour {
  id: number;
  name: string;
  location: string;
  price: number;
}

interface Booking {
  id: number;
  user_id: number;
  tour: Tour;
  number_people: number;
  total_price: number;
  status: string;
  created_at?: string;
}

const tour_id = ref<number | null>(null);
const number_people = ref<number>(1);
const booking = ref<Booking | null>(null);

const router = useRouter();

async function doBooking() {
  if (!tour_id.value || number_people.value <= 0) {
    alert("⚠️ Vui lòng nhập đầy đủ thông tin hợp lệ");
    return;
  }
  try {
    const res = await api.post("/bookings/", {
      tour_id: tour_id.value,
      number_people: number_people.value,
    });
    booking.value = res.data;
    alert("✅ Booking thành công!");
  } catch (err: any) {
    alert(err.response?.data?.detail || "Booking thất bại");
    booking.value = null;
  }
}

function goToPayment() {
  if (!booking.value) return;
  router.push({
    path: "/payment",
    query: {
      booking_id: booking.value.id,
      amount: booking.value.total_price,
    },
  });
}

function goToTours() {
  router.push("/tours");
}

// Định dạng tiền tệ chuẩn VND
const formattedTotalPrice = computed(() => {
  if (!booking.value) return "";
  return booking.value.total_price.toLocaleString("vi-VN") + " ₫";
});

// Stats giả lập
const totalBookings = ref(124);
const totalVisitors = ref(89);

// Thông tin du lịch
const travelCards = ref([
  { title: "🏞️ Địa danh nổi bật", content: "Hạ Long, Hội An, Phú Quốc, Sapa… thu hút hàng triệu khách mỗi năm." },
  { title: "🧳 Mẹo du lịch", content: "Đặt vé trước để tiết kiệm, mang theo thuốc chống côn trùng, chuẩn bị trang phục theo mùa." },
  { title: "🎉 Lễ hội & sự kiện", content: "Tết Nguyên Đán, Chùa Hương, Lễ hội đèn lồng Hội An… hàng nghìn lượt khách tham dự." },
  { title: "🍲 Ẩm thực nổi bật", content: "Phở Hà Nội, Bún Bò Huế, Bánh xèo miền Nam… món đặc sản được yêu thích." },
  { title: "🏖️ Bãi biển đông đảo", content: "Phú Quốc, Nha Trang, Đà Nẵng luôn đông khách vào mùa hè." },
  { title: "🥾 Hoạt động nổi bật", content: "Trekking Sapa, leo Fansipan, lặn biển Phú Quốc, tham quan phố cổ Hội An." },
  { title: "🛶 Du lịch miền Tây", content: "Chợ nổi Cái Răng, sông Mekong, trải nghiệm cuộc sống miền sông nước." },
  { title: "🏯 Văn hóa & lịch sử", content: "Huế, cố đô, các đền, chùa truyền thống, bảo tàng lịch sử." },
  { title: "🏔️ Khám phá núi rừng", content: "Đà Lạt, Fansipan, Ba Vì… trekking, dã ngoại, cắm trại." },
  { title: "🌅 Ngắm bình minh & hoàng hôn", content: "Bãi biển Nha Trang, Hội An, Tam Đảo, các điểm ngắm cảnh tuyệt đẹp." }
]);

// Hiệu ứng khi scroll
onMounted(() => {
  const cards = document.querySelectorAll(".info-card");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );
  cards.forEach((card) => observer.observe(card));
});
</script>

<style scoped>
/* Giữ nguyên toàn bộ style như trước */
.booking-page {
  font-family: Arial, sans-serif;
  position: relative;
}
.background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1950&q=80') center/cover no-repeat;
  filter: blur(8px) brightness(0.7);
  z-index: -1;
}
.container {
  max-width: 1200px;
  margin: 2rem auto;
  position: relative;
  z-index: 1;
}
.booking-container {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}
.left-column {
  flex: 1;
}
.slogan h2 {
  font-size: 1.8rem;
  color: #1976d2;
  margin-bottom: 0.5rem;
}
.slogan p {
  color: #555;
  margin-bottom: 1rem;
}
.booking-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}
.form-group label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.form-group input[type="number"] {
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.submit-btn,
.pay-btn,
.view-tours-btn {
  padding: 0.9rem 1rem;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s, transform 0.2s;
}
.submit-btn:hover,
.pay-btn:hover,
.view-tours-btn:hover {
  transform: translateY(-2px);
}
.pay-btn {
  margin-top: 1rem;
  background: #2e7d32;
}
.tips {
  background: rgba(255,255,255,0.95);
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 10px;
  box-shadow: 0 3px 12px rgba(0,0,0,0.1);
}
.tips ul {
  padding-left: 1.2rem;
  margin: 0;
}
.stats {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.stat-card {
  flex: 1;
  background: rgba(240,244,248,0.95);
  padding: 0.8rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 3px 12px rgba(0,0,0,0.1);
}
.stat-card h4 {
  margin: 0;
  font-size: 1.2rem;
  color: #1976d2;
}
.stat-card p {
  margin: 0;
  color: #555;
  font-size: 0.9rem;
}
.booking-info {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(227, 247, 227, 0.95);
  border-radius: 10px;
  line-height: 1.6;
}
.cta {
  margin-top: 1rem;
}
.right-column {
  flex: 1;
}
.right-column h3 {
  margin-bottom: 1rem;
  color: #1976d2;
}
.info-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.info-card {
  padding: 1rem;
  background: rgba(240,244,248,0.95);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.info-card.visible {
  opacity: 1;
  transform: translateY(0);
}
.info-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
@media (max-width: 992px) {
  .booking-container {
    flex-direction: column;
  }
}
</style>
