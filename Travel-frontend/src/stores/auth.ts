import { reactive } from "vue";

// ✅ Store quản lý trạng thái đăng nhập
export const authStore = reactive({
  user: null as null | { id: number; name: string; email: string; role?: string },

  // Gán thông tin user sau khi đăng nhập
  setUser(user: any) {
    this.user = user;
    localStorage.setItem("user", JSON.stringify(user));
  },

  // Lấy user hiện tại
  getUser() {
    if (!this.user) {
      const storedUser = localStorage.getItem("user");
      if (storedUser) {
        this.user = JSON.parse(storedUser);
      }
    }
    return this.user;
  },

  // Đăng xuất
  logout() {
    this.user = null;
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
  },
});
