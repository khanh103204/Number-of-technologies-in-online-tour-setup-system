<template>
  <div id="app">
    <!-- THANH NAVBAR -->
    <Navbar />

    <!-- NỘI DUNG CHÍNH -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- CHÂN TRANG -->
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";
</script>

<style>
/* Reset mặc định */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Cấu trúc tổng thể */
html, body, #app {
  width: 100%;
  min-height: 100%;
  font-family: "Inter", Arial, sans-serif;
  background-color: #f5f7fa;
  color: #222;
  display: flex;
  flex-direction: column;
}

/* Nội dung chính (để Footer luôn nằm cuối) */
.main-content {
  flex: 1;
  padding-bottom: 40px;
}

/* Liên kết mặc định */
a {
  text-decoration: none;
  color: inherit;
}

/* Cuộn mượt */
html {
  scroll-behavior: smooth;
}
</style>
