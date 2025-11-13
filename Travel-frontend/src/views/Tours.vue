<template>
  <div class="tours-page">
    <!-- 1️⃣ HERO -->
    <section class="hero">
      <div class="overlay">
        <h1>Khám phá thế giới cùng TravelNow</h1>
        <p>Tìm kiếm và đặt tour phù hợp với bạn chỉ trong vài giây</p>
        <div class="search-box">
          <input
            v-model="search"
            type="text"
            placeholder="Nhập nơi bạn muốn đến "
          />
          <button @click="filterTours">Tìm kiếm</button>
        </div>
      </div>
    </section>

    <!-- 🔎 KẾT QUẢ TÌM KIẾM -->
    <section v-if="searchResults.length" class="tour-list">
      <h2>Kết quả tìm kiếm cho "{{ search }}"</h2>
      <div class="tour-grid">
        <router-link
          v-for="tour in searchResults"
          :key="tour.id"
          :to="{ name: 'TourDetail', params: { id: tour.id } }"
          class="tour-card"
        >
          <img :src="tour.image" :alt="tour.title" />
          <h3>{{ tour.title }}</h3>
          <p class="location">📍 {{ tour.location }}</p>
          <p class="price">{{ tour.price.toLocaleString() }} đ</p>
        </router-link>
      </div>
    </section>

    <!-- 2️⃣ TOUR TRONG NƯỚC -->
    <section class="tour-list" v-else>
      <h2>Tour du lịch trong nước được yêu thích</h2>

      <div class="category-tabs">
        <button
          v-for="c in domesticCategories"
          :key="c"
          @click="selectedDomestic = c"
          :class="{ active: selectedDomestic === c }"
        >
          {{ c }}
        </button>
      </div>

      <div class="tour-grid">
        <router-link
          v-for="tour in filteredDomestic"
          :key="tour.id"
          :to="{ name: 'TourDetail', params: { id: tour.id } }"
          class="tour-card"
        >
          <img :src="tour.image" :alt="tour.title" />
          <h3>{{ tour.title }}</h3>
          <p class="location">📍 {{ tour.location }}</p>
          <p class="price">{{ tour.price.toLocaleString() }} đ</p>
        </router-link>
      </div>
    </section>

    <!-- 3️⃣ VIỆT NAM ĐỆ NHẤT -->
    <section class="tour-list" v-if="!searchResults.length">
      <h2>🇻🇳 Việt Nam đệ nhất trứ danh</h2>
      <p class="subtitle">Đi đến những nơi ấn tượng nhất của Việt Nam</p>

      <div class="category-tabs">
        <button
          v-for="c in vnCategories"
          :key="c"
          @click="selectedVNCategory = c"
          :class="{ active: selectedVNCategory === c }"
        >
          {{ c }}
        </button>
      </div>

      <div class="tour-grid">
        <router-link
          v-for="tour in filteredVNTours"
          :key="tour.id"
          :to="{ name: 'TourDetail', params: { id: tour.id } }"
          class="tour-card"
        >
          <img :src="tour.image" :alt="tour.title" />
          <h3>{{ tour.title }}</h3>
          <p class="location">📍 {{ tour.location }}</p>
          <p class="price">{{ tour.price.toLocaleString() }} đ</p>
        </router-link>
      </div>
    </section>

    <!-- 4️⃣ TOUR YÊU THÍCH -->
    <section class="tour-list popular" v-if="!searchResults.length">
      <h2>🔥 Tour được yêu thích nhiều nhất</h2>
      <p class="subtitle">Khám phá những tour du lịch hot nhất hiện nay</p>

      <div class="tour-grid">
        <router-link
          v-for="tour in popularTours"
          :key="tour.id"
          :to="{ name: 'TourDetail', params: { id: tour.id } }"
          class="tour-card"
        >
          <img :src="tour.image" :alt="tour.title" />
          <h3>{{ tour.title }}</h3>
          <p class="location">📍 {{ tour.location }}</p>
          <p class="price">{{ tour.price.toLocaleString() }} đ</p>
        </router-link>
      </div>
    </section>

    <!-- 5️⃣ GIỚI THIỆU -->
    <section class="intro-section" v-if="!searchResults.length">
      <div class="intro-container">
        <div class="left-box">
          <h3>Khám phá TravelNow</h3>
          <p>Sống giàu trải nghiệm cùng TravelNow</p>
          <h4>Tại sao nên đặt tour du lịch với TravelNow?</h4>
          <ol>
            <li>Hơn 32.000 hoạt động vui chơi toàn cầu</li>
            <li>Đặt trực tuyến, miễn xếp hàng</li>
            <li>Phương thức thanh toán đa dạng</li>
            <li>Tích điểm thành viên</li>
            <li>TravelNow Priority</li>
            <li>Bảo mật thông tin khách hàng</li>
            <li>Chăm sóc khách hàng tận tâm</li>
            <li>Ưu đãi mỗi ngày</li>
          </ol>
        </div>

        <div class="right-content">
          <h2>Sống giàu trải nghiệm cùng TravelNow</h2>
          <p>
            Du lịch không chỉ là việc đến một nơi xa lạ, mà còn là hành trình khám phá và tận hưởng.
            Với TravelNow, bạn sẽ được đắm chìm trong những trải nghiệm đáng nhớ.
          </p>
          <ul>
            <li>✔️ Hơn 32.000 tour và hoạt động trên toàn cầu</li>
            <li>✔️ Hỗ trợ khách hàng 24/7</li>
            <li>✔️ Thanh toán nhanh chóng, an toàn</li>
            <li>✔️ Ưu đãi đặc biệt dành cho thành viên</li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

interface Tour {
  id: number;
  title: string;
  location: string;
  price: number;
  image: string;
}

/* --- DỮ LIỆU MẪU --- */
const domesticTours = ref<Tour[]>([
  { id: 1, title: "Khám phá 2 đảo, Sun World Hòn Thơm", location: "Phú Quốc", price: 1404000, image: "phuquoc.jpeg" },
  { id: 2, title: "Tour 3 đảo bằng Cano Nam Phú Quốc", location: "Phú Quốc", price: 800000, image: "daohonthom.jpg" },
  { id: 3, title: "Tour khám phá 3 đảo bằng tàu", location: "Phú Quốc", price: 605000, image: "phuquoc3.jpg" },
  { id: 4, title: "Tour ngắm hoàng hôn và câu mực", location: "Phú Quốc", price: 271000, image: "phuquoc2.jpg" },
  { id: 5, title: "Tour Cắm Trại Hòn Gầm Ghì - Hòn Mây Rút", location: "Phú Quốc", price: 1967000, image: "phuquoc5.jpg" },
]);

const vnTours = ref<Tour[]>([
  { id: 6, title: "Sun World Ba Na Hills tại Đà Nẵng", location: "Đà Nẵng", price: 625100, image: "danang.jpg" },
  { id: 7, title: "Vé Show Ký Ức Hội An", location: "Hội An", price: 108000, image: "hoian.jpg" },
  { id: 8, title: "Vé VinWonders Nam Hội An", location: "Hội An", price: 300000, image: "namhoian.jpg" },
  { id: 9, title: "Da Nang Mikazuki Water Park 365", location: "Đà Nẵng", price: 250000, image: "danangwater.png" },
  { id: 10, title: "Núi Thần Tài Hot Springs Park", location: "Đà Nẵng", price: 185250, image: "nuithantai.jpg" },
]);

const popularTours = ref<Tour[]>([
  { id: 11, title: "Khám phá Đà Lạt 3N2Đ", location: "Đà Lạt", price: 1450000, image: "dalat1.jpg" },
  { id: 12, title: "Tour Hà Giang – Mã Pì Lèng", location: "Hà Giang", price: 1850000, image: "hagiang.jpg" },
  { id: 13, title: "Khám phá Nha Trang – Vinpearl Land", location: "Nha Trang", price: 950000, image: "nhatrang1.jpg" },
  { id: 14, title: "Du lịch Sapa - Bản Cát Cát", location: "Sapa", price: 1300000, image: "sapa.jpg" },
  { id: 15, title: "Tour Tràng An – Ninh Bình", location: "Ninh Bình", price: 1100000, image: "ninhbinh.jpg" },
]);

const domesticCategories = ref(["Phú Quốc", "Nha Trang", "Đà Nẵng", "Đà Lạt", "Ninh Bình-Hạ Long", "Sapa-Hà Giang"]);
const selectedDomestic = ref("Phú Quốc");

const vnCategories = ref(["Tất cả", "Đà Nẵng", "Hội An"]);
const selectedVNCategory = ref("Tất cả");

const search = ref("");
const searchResults = ref<Tour[]>([]);

const filteredDomestic = computed(() =>
  domesticTours.value.filter(
    (tour) => selectedDomestic.value === tour.location || selectedDomestic.value === "Tất cả"
  )
);

const filteredVNTours = computed(() =>
  vnTours.value.filter(
    (tour) => selectedVNCategory.value === "Tất cả" || tour.location === selectedVNCategory.value
  )
);

function filterTours() {
  if (!search.value.trim()) {
    searchResults.value = [];
    return;
  }

  const keyword = search.value.toLowerCase();
  const allTours = [...domesticTours.value, ...vnTours.value, ...popularTours.value];

  searchResults.value = allTours.filter(
    (tour) =>
      tour.title.toLowerCase().includes(keyword) ||
      tour.location.toLowerCase().includes(keyword)
  );
}
</script>

<style scoped>
.hero {
  position: relative;
  height: 420px;
  background: url("halong.jpg") center/cover no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
}
.overlay {
  text-align: center;
  color: white;
  background: rgba(0, 0, 0, 0.45);
  padding: 36px;
  border-radius: 12px;
}
.search-box {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 14px;
}
.search-box input {
  padding: 10px 14px;
  width: 420px;
  border-radius: 6px;
  border: none;
}
.search-box button {
  background: #0f62fe;
  color: white;
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.tour-list {
  padding: 40px 80px;
  background: #fff;
}
.tour-list h2 {
  margin-bottom: 12px;
  color: #222;
  font-weight: 700;
}
.subtitle {
  color: #666;
  margin-bottom: 20px;
}
.category-tabs {
  margin-bottom: 20px;
}
.category-tabs button {
  margin-right: 10px;
  padding: 8px 18px;
  border-radius: 30px;
  border: 1px solid #eee;
  cursor: pointer;
  background: #f9f9f9;
}
.category-tabs button.active {
  background: #ffecec;
  color: #ff6b6b;
  border-color: #ff6b6b;
}
.tour-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}
.tour-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: all 0.2s;
  text-decoration: none;
  color: inherit;
}
.tour-card:hover {
  transform: translateY(-5px);
}
.tour-card img {
  width: 100%;
  height: 140px;
  object-fit: cover;
}
.tour-card h3 {
  font-size: 15px;
  padding: 10px;
  color: #111;
}
.location {
  padding: 0 10px;
  color: #777;
  font-size: 13px;
}
.price {
  padding: 0 10px 10px;
  font-weight: bold;
  color: #e53935;
}
.popular {
  background: #f9fafc;
}
.intro-section {
  background: #f9fafc;
  padding: 60px 80px;
  display: flex;
  justify-content: center;
}
.intro-container {
  display: flex;
  gap: 50px;
  max-width: 1200px;
}
.left-box {
  background: #fff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  width: 320px;
  flex-shrink: 0;
}
.right-content {
  flex: 1;
  color: #333;
}
.right-content h2 {
  font-size: 24px;
  color: #111;
  margin-bottom: 10px;
}
.right-content p {
  line-height: 1.6;
  margin-bottom: 12px;
}
</style>
