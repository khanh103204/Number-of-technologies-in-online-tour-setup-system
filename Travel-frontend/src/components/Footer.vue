<template>
  <footer class="footer">
    <!-- Sóng động -->
    <div class="wave wave1"></div>
    <div class="wave wave2"></div>
    <div class="wave wave3"></div>

    <!-- Nội dung chính -->
    <div class="footer-content">
      <!-- Giới thiệu -->
      <div class="footer-section about">
        <h2 class="logo">Travel<span>Now</span></h2>
        <p>
          TravelNow mang đến trải nghiệm đặt tour hiện đại, giúp bạn khám phá
          thế giới một cách dễ dàng, nhanh chóng và đáng tin cậy.
        </p>
        <div class="social-icons">
          <a href="#" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
          <a href="#" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
          <a href="#" aria-label="TikTok"><i class="fa-brands fa-tiktok"></i></a>
          <a href="#" aria-label="YouTube"><i class="fa-brands fa-youtube"></i></a>
          <a href="#" aria-label="Telegram"><i class="fa-brands fa-telegram"></i></a>
        </div>
      </div>

      <!-- Liên kết nhanh -->
      <div class="footer-section links">
        <h3>Liên kết nhanh</h3>
        <ul>
          <li><a href="#">Trang chủ</a></li>
          <li><a href="#">Tour nổi bật</a></li>
          <li><a href="#">Giới thiệu</a></li>
          <li><a href="#">Liên hệ</a></li>
          <li><a href="#">Hỗ trợ</a></li>
        </ul>
      </div>

      <!-- Dịch vụ -->
      <div class="footer-section services">
        <h3>Dịch vụ</h3>
        <ul>
          <li><a href="#">Đặt tour</a></li>
          <li><a href="#">Khách sạn</a></li>
          <li><a href="#">Vé máy bay</a></li>
          <li><a href="#">Cho thuê xe</a></li>
          <li><a href="#">Combo du lịch</a></li>
        </ul>
      </div>

      <!-- Ứng dụng di động -->
      <div class="footer-section app">
        <h3>Tải ứng dụng TravelNow</h3>
        <p>Trải nghiệm đặt tour dễ dàng hơn với ứng dụng của chúng tôi!</p>
        <div class="app-buttons">
          <a href="#" class="store-btn google">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play" />
          </a>
          <a href="#" class="store-btn apple">
            <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" alt="App Store" />
          </a>
        </div>

        <h3 style="margin-top: 20px;">Đăng ký nhận tin</h3>
        <div class="newsletter-box">
          <input type="email" placeholder="Nhập email của bạn" />
          <button><i class="fa-solid fa-paper-plane"></i></button>
        </div>
      </div>
    </div>

    <!-- Dưới cùng -->
    <div class="footer-bottom">
      <p>© 2025 <strong>TravelNow</strong>. All rights reserved.</p>
      <div class="payment-icons">
        <i class="fa-brands fa-cc-visa"></i>
        <i class="fa-brands fa-cc-mastercard"></i>
        <i class="fa-brands fa-cc-paypal"></i>
        <i class="fa-brands fa-cc-amex"></i>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
.footer {
  position: relative;
  background: linear-gradient(135deg, #06223d, #0a315c, #0d447c);
  color: #e5ecf3;
  padding-top: 120px;
  overflow: hidden;
  font-family: 'Poppins', sans-serif;
  animation: gradientMove 10s ease infinite alternate;
}

@keyframes gradientMove {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}

/* 🌊 Hiệu ứng sóng */
.wave {
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100px;
  background: url('https://svgshare.com/i/uXx.svg');
  background-size: 50% 100px;
  opacity: 0.25;
  animation: waveMove 12s linear infinite;
}
.wave1 {
  top: 0;
  animation-delay: 0s;
}
.wave2 {
  top: 10px;
  opacity: 0.3;
  animation-delay: -3s;
}
.wave3 {
  top: 20px;
  opacity: 0.15;
  animation-delay: -6s;
}

@keyframes waveMove {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-25%);
  }
}

/* 📦 Nội dung chính */
.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 50px;
  padding: 0 60px 60px;
  position: relative;
  z-index: 2;
}

/* Các section */
.footer-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 14px;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section li {
  margin-bottom: 8px;
}

.footer-section a {
  color: #c4d6e3;
  text-decoration: none;
  transition: color 0.3s;
}
.footer-section a:hover {
  color: #00aaff;
}

/* Logo và mô tả */
.about .logo {
  font-size: 30px;
  font-weight: 700;
  color: white;
}
.about .logo span {
  color: #00aaff;
}
.about p {
  font-size: 14px;
  margin: 10px 0 15px;
  line-height: 1.5;
}

/* Social */
.social-icons {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}
.social-icons a {
  color: #b0c4d4;
  font-size: 18px;
  border: 1px solid #2a3b50;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}
.social-icons a:hover {
  background: #00aaff;
  color: white;
  transform: translateY(-3px);
}

/* App download */
.app-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}
.app-buttons img {
  width: 150px;
  transition: transform 0.3s;
}
.app-buttons img:hover {
  transform: scale(1.05);
}

/* Newsletter */
.newsletter-box {
  display: flex;
  align-items: center;
  border: 1px solid #2a3b50;
  border-radius: 30px;
  overflow: hidden;
  margin-top: 10px;
}
.newsletter-box input {
  flex: 1;
  padding: 10px 15px;
  background: transparent;
  border: none;
  outline: none;
  color: #fff;
}
.newsletter-box button {
  background: #00aaff;
  border: none;
  color: white;
  padding: 10px 14px;
  cursor: pointer;
  transition: background 0.3s;
}
.newsletter-box button:hover {
  background: #0091d1;
}

/* Footer bottom */
.footer-bottom {
  border-top: 1px solid #1d2a3a;
  padding: 18px 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  font-size: 13px;
  color: #9fb2c3;
}
.payment-icons i {
  font-size: 24px;
  margin-left: 10px;
  color: #9fb2c3;
  transition: color 0.3s;
}
.payment-icons i:hover {
  color: #00aaff;
}

/* Responsive */
@media (max-width: 768px) {
  .footer-content {
    padding: 0 20px 50px;
  }
  .footer-bottom {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
}
</style>
