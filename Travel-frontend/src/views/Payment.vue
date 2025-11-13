<template>
  <div class="payment-page">
    <div class="background-overlay"></div>

    <div class="container">
      <!-- Form thanh toán -->
      <div class="payment-card">
        <h2>💳 Thanh toán an toàn</h2>
        <p>🔒 Chọn phương thức, xác nhận và thanh toán nhanh chóng!</p>

        <form @submit.prevent="doPay" class="payment-form">
          <!-- Booking ID -->
          <div class="form-group">
            <label for="bookingId">Mã đặt chỗ (Booking ID)</label>
            <div class="input-wrapper">
              <span class="icon">🆔</span>
              <input id="bookingId" v-model.number="booking_id" type="number" readonly />
            </div>
          </div>

          <!-- Số tiền -->
          <div class="form-group">
            <label for="amount">Số tiền</label>
            <div class="input-wrapper">
              <span class="icon">💰</span>
              <input
                id="amount"
                :value="formattedAmount"
                readonly
              />
            </div>
          </div>

          <!-- Phương thức thanh toán -->
          <div class="form-group">
            <label for="method">Phương thức thanh toán</label>
            <div class="input-wrapper">
              <span class="icon">💳</span>
              <select id="method" v-model="method">
                <option value="VNPay">VNPay</option>
                <option value="Momo">Momo</option>
                <option value="Visa">Visa/Thẻ</option>
                <option value="QR">QR</option>
              </select>
            </div>
          </div>

          <button type="submit" class="submit-btn">Thanh toán</button>
        </form>

        <!-- Thông tin thanh toán -->
        <div v-if="payment" class="payment-info">
          <h3>✅ Thanh toán thành công!</h3>
          <p><strong>ID:</strong> {{ payment.id }}</p>
          <p><strong>Booking ID:</strong> {{ payment.booking_id }}</p>
          <p><strong>Số tiền:</strong> {{ formatVND(payment.amount) }}</p>
          <p><strong>Phương thức:</strong> {{ payment.method }}</p>
          <p><strong>Trạng thái:</strong> {{ payment.status }}</p>
          <p><strong>Ngày thanh toán:</strong> {{ payment.paid_at }}</p>
          <p><strong>Ngày tạo:</strong> {{ payment.created_at }}</p>
        </div>
      </div>

      <!-- Ưu đãi thanh toán -->
      <div class="payment-tips">
        <h3>🎁 Ưu đãi khi thanh toán</h3>
        <div class="tip-card" v-for="(card,i) in paymentTips" :key="i">
          <h4>{{ card.title }}</h4>
          <p>{{ card.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import api from "../api/axios";

interface Payment {
  id: number;
  booking_id: number;
  amount: number;
  method: "VNPay" | "Momo" | "Visa" | "QR";
  status: string;
  paid_at?: string;
  created_at?: string;
}

const route = useRoute();
const booking_id = ref<number | null>(null);
const amount = ref<number>(0);
const method = ref<Payment["method"]>("VNPay");
const payment = ref<Payment | null>(null);

// Format tiền VND
function formatVND(value: number): string {
  return value.toLocaleString("vi-VN", {
    style: "currency",
    currency: "VND",
    minimumFractionDigits: 0,
  });
}

const formattedAmount = computed(() => formatVND(amount.value));

onMounted(() => {
  const query = route.query;
  if (query.booking_id) booking_id.value = Number(query.booking_id);
  if (query.amount) amount.value = Number(query.amount);
});

// Thanh toán
async function doPay() {
  if (!booking_id.value || booking_id.value <= 0) {
    alert("⚠️ Booking ID không hợp lệ!");
    return;
  }
  if (amount.value <= 0) {
    alert("⚠️ Số tiền không hợp lệ!");
    return;
  }

  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Vui lòng đăng nhập trước khi thanh toán!");
    return;
  }

  try {
    const res = await api.post(
      "/payments/",
      {
        booking_id: booking_id.value,
        amount: amount.value,
        method: method.value,
      },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    payment.value = res.data;
    alert("🎉 Thanh toán thành công!");
  } catch (err: any) {
    console.error(err);
    alert(err.response?.data?.detail || "Thanh toán thất bại");
    payment.value = null;
  }
}

// Ưu đãi thanh toán
const paymentTips = ref([
  {
    title: "VNPay",
    content:
      "🎉 Giảm 5% tất cả tour, voucher 100k cho đơn đầu tiên.\n🏖️ -50% tour Hạ Long 2N1Đ từ 1/11 đến 30/11.\n🎁 Thanh toán qua VNPay QR, miễn phí giao dịch.",
  },
  {
    title: "Momo",
    content:
      "💸 Nhận voucher 50.000 VND cho lần đầu.\n🏝️ Giảm 30% tour Phú Quốc mùa hè.\n🎉 Tích điểm Momo Rewards khi thanh toán.",
  },
  {
    title: "Visa/Thẻ quốc tế",
    content:
      "💳 Hoàn tiền 3% tối đa 200.000 VND.\n🏞️ Tour Sapa, Đà Lạt giảm thêm 10% cuối tuần.\n🔒 Bảo mật 3D Secure.",
  },
  {
    title: "QR Code",
    content:
      "📱 Thanh toán qua QR nhận ưu đãi 2% tất cả tour.\n🎁 Miễn phí phí giao dịch trên 500.000 VND.",
  },
  {
    title: "Ngân hàng Agribank",
    content:
      "🏦 Hoàn 1% cho mọi đơn hàng.\n🎫 Tặng 100.000 VND voucher trên 2.000.000 VND.\n🏖️ -20% tour Đà Nẵng 3N2Đ khi thanh toán qua app.",
  },
  {
    title: "Techcombank",
    content:
      "🏝️ Giảm 15% tour Hội An 2N1Đ.\n💰 Miễn phí chuyển khoản.\n🎉 Quà tặng đặc biệt cho đơn trên 3.000.000 VND.",
  },
]);

// Parallax background
onMounted(() => {
  const bg = document.querySelector(".background-overlay") as HTMLElement;
  window.addEventListener("scroll", () => {
    const scroll = window.scrollY;
    if (bg) bg.style.transform = `translateY(${scroll * 0.2}px)`;
  });
});
</script>

<style scoped>
.payment-page {
  font-family: "Inter", Arial, sans-serif;
  position: relative;
}

.background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 150%;
  background: url('https://images.unsplash.com/photo-1556740749-887f6717d7e4?auto=format&fit=crop&w=1950&q=80')
    center/cover no-repeat;
  filter: brightness(0.7) blur(5px);
  z-index: -1;
  transform: translateY(0);
  transition: transform 0.2s ease-out;
}

.container {
  max-width: 1000px;
  margin: 2rem auto;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
  z-index: 1;
  position: relative;
}

.payment-card {
  flex: 1 1 400px;
  background: linear-gradient(145deg, #ffffff, #e0f7fa);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2);
}

.payment-card h2 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.payment-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-wrapper {
  position: relative;
}

.input-wrapper .icon {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
}

.input-wrapper input,
.input-wrapper select {
  width: 100%;
  padding: 0.6rem 0.6rem 0.6rem 2rem;
  border-radius: 10px;
  border: 1px solid #ccc;
  transition: 0.3s;
}

.input-wrapper input:focus,
.input-wrapper select:focus {
  border-color: #1976d2;
  box-shadow: 0 0 8px rgba(25, 118, 210, 0.3);
  outline: none;
}

.submit-btn {
  padding: 0.9rem;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: 0.3s;
}

.submit-btn:hover {
  background: #145ca8;
  transform: translateY(-2px);
}

.payment-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(227, 247, 227, 0.95);
  border-radius: 12px;
}

.payment-tips {
  flex: 1 1 300px;
}

.tip-card {
  background: rgba(240, 244, 248, 0.95);
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  white-space: pre-line;
  transition: 0.3s;
}

.tip-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

@media (max-width: 992px) {
  .container {
    flex-direction: column;
    align-items: center;
  }
}
</style>
