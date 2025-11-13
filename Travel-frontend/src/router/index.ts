import { createRouter, createWebHistory } from "vue-router";

// 🧭 Import các trang
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Tours from "../views/Tours.vue";
import TourDetail from "../views/TourDetail.vue";
import Recommend from "../views/Recommend.vue";
import Booking from "../views/Booking.vue";
import Payment from "../views/Payment.vue";
import Admin from "../views/Admin.vue";
import MyBookings from "../views/MyBookings.vue";

// 🗺️ Khai báo routes
const routes = [
  { path: "/", redirect: "/tours" },

  { path: "/login", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },

  { path: "/tours", name: "Tours", component: Tours },
  { path: "/tours/:id", name: "TourDetail", component: TourDetail, props: true },

  { path: "/recommend", name: "Recommend", component: Recommend },
  { path: "/booking", name: "Booking", component: Booking },
  { path: "/payment", name: "Payment", component: Payment },

  { path: "/my-bookings", name: "MyBookings", component: MyBookings },

  // Admin route
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    meta: { requiresAdmin: true }, // 🔒 chỉ admin được phép vào
  },

  // Route không tồn tại → redirect về /tours
  { path: "/:pathMatch(.*)*", redirect: "/tours" },
];

// 🚀 Tạo router
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

// 🔐 Middleware kiểm tra quyền truy cập admin
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAdmin) {
    const token = localStorage.getItem("access_token");
    const userRaw = localStorage.getItem("user");

    if (!token || !userRaw) {
      alert("⚠️ Vui lòng đăng nhập với quyền admin!");
      return next({ name: "Login" });
    }

    try {
      const user = JSON.parse(userRaw);
      const role = (user.role || "").toLowerCase();

      if (role !== "admin") {
        alert("🚫 Bạn không có quyền truy cập trang quản trị!");
        return next({ name: "Tours" });
      }
    } catch (err) {
      console.error("❌ Lỗi đọc thông tin người dùng:", err);
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      alert("Phiên đăng nhập không hợp lệ, vui lòng đăng nhập lại!");
      return next({ name: "Login" });
    }
  }

  next();
});

export default router;
