<template>
  <div class="admin-page">
    <h2>Trang quản trị</h2>

    <!-- Nếu không phải admin -->
    <div v-if="!isAdmin" class="no-access">
      <p>Bạn không có quyền truy cập trang quản trị!</p>
    </div>

    <!-- Nếu là admin -->
    <div v-else>
      <!-- Form thêm tour -->
      <form @submit.prevent="addTour" class="tour-form">
        <h3>➕ Thêm Tour Mới</h3>

        <div class="form-grid">
          <div class="form-group">
            <label>Tên tour</label>
            <input v-model="newTour.name" placeholder="Nhập tên tour" required />
          </div>

          <div class="form-group">
            <label>Địa điểm</label>
            <input v-model="newTour.location" placeholder="Ví dụ: Đà Nẵng, Nha Trang..." required />
          </div>

          <div class="form-group">
            <label>Loại tour</label>
            <input v-model="newTour.type" placeholder="Biển, Núi, Văn hóa..." required />
          </div>
        </div>

        <div class="form-group">
          <label>Mô tả chi tiết</label>
          <textarea
            v-model="newTour.description"
            placeholder="Mô tả chi tiết về tour"
            rows="3"
          ></textarea>
        </div>

        <div class="form-grid">
          <div class="form-group">
            <label>Giá tour (VND)</label>
            <input v-model.number="newTour.price" type="number" placeholder="Nhập giá" required />
          </div>
          <div class="form-group">
            <label>Số người tối thiểu</label>
            <input v-model.number="newTour.min_people" type="number" required />
          </div>
          <div class="form-group">
            <label>Số người tối đa</label>
            <input v-model.number="newTour.max_people" type="number" required />
          </div>
        </div>

        <div class="form-grid">
          <div class="form-group">
            <label>Số ngày</label>
            <input v-model.number="newTour.duration_days" type="number" required />
          </div>
          <div class="form-group">
            <label>Độ khó</label>
            <select v-model="newTour.difficulty" required>
              <option disabled value="">-- Chọn độ khó --</option>
              <option value="easy">Dễ</option>
              <option value="medium">Trung bình</option>
              <option value="hard">Khó</option>
            </select>
          </div>
          <div class="form-group">
            <label>Đánh giá trung bình (0-5)</label>
            <input v-model.number="newTour.rating_avg" type="number" step="0.1" />
          </div>
        </div>

        <label class="checkbox">
          <input type="checkbox" v-model="newTour.available" />
          Còn hoạt động
        </label>

        <button type="submit" class="btn-submit">+ Thêm Tour</button>
      </form>

      <!-- Danh sách tour -->
      <h3>📋 Danh sách tour</h3>
      <table class="tour-table">
        <thead>
          <tr>
            <th>Tên tour</th>
            <th>Địa điểm</th>
            <th>Loại</th>
            <th>Giá (VND)</th>
            <th>Số người</th>
            <th>Số ngày</th>
            <th>Độ khó</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tour in tours" :key="tour.id">
            <td>{{ tour.name }}</td>
            <td>{{ tour.location }}</td>
            <td>{{ tour.type }}</td>
            <td>{{ formatCurrency(tour.price) }}</td>
            <td>{{ tour.min_people }} - {{ tour.max_people }}</td>
            <td>{{ tour.duration_days }}</td>
            <td>{{ tour.difficulty }}</td>
            <td>
              <span :class="tour.available ? 'active' : 'inactive'">
                {{ tour.available ? "Còn hoạt động" : "Ngừng" }}
              </span>
            </td>
            <td class="action-buttons">
              <button @click="prepareEdit(tour)" class="btn-edit">✏️ Sửa</button>
              <button @click="deleteTour(tour.id)" class="btn-delete">🗑️ Xóa</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Popup chỉnh sửa -->
      <div v-if="editingTour" class="popup">
        <div class="popup-content">
          <h3>Chỉnh sửa tour</h3>

          <div class="form-grid">
            <div class="form-group">
              <label>Tên</label>
              <input v-model="editForm.name" />
            </div>
            <div class="form-group">
              <label>Địa điểm</label>
              <input v-model="editForm.location" />
            </div>
            <div class="form-group">
              <label>Loại</label>
              <input v-model="editForm.type" />
            </div>
            <div class="form-group">
              <label>Giá</label>
              <input v-model.number="editForm.price" type="number" />
            </div>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label>Tối thiểu</label>
              <input v-model.number="editForm.min_people" type="number" />
            </div>
            <div class="form-group">
              <label>Tối đa</label>
              <input v-model.number="editForm.max_people" type="number" />
            </div>
            <div class="form-group">
              <label>Số ngày</label>
              <input v-model.number="editForm.duration_days" type="number" />
            </div>
          </div>

          <div class="popup-actions">
            <button class="btn-primary" @click="saveEdit">Lưu</button>
            <button class="btn-cancel" @click="cancelEdit">Hủy</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  name: "AdminPage",
  data() {
    return {
      isAdmin: false,
      tours: [],
      editingTour: false,
      editForm: {},

      newTour: {
        name: "",
        location: "", // 🆕 thêm location
        description: "",
        price: 0,
        type: "",
        min_people: 1,
        max_people: 10,
        duration_days: 3,
        difficulty: "",
        rating_avg: 0,
        available: true,
      },
    };
  },
  methods: {
    safeDecodeToken(token) {
      try {
        const base64Url = token.split(".")[1];
        const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split("")
            .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
            .join("")
        );
        return JSON.parse(jsonPayload);
      } catch {
        return null;
      }
    },

    formatCurrency(v) {
      const n = Number(v);
      return isNaN(n) ? v : n.toLocaleString("vi-VN");
    },

    async checkAdmin() {
      const token =
        localStorage.getItem("access_token") || localStorage.getItem("token");
      if (!token) return (this.isAdmin = false);
      const payload = this.safeDecodeToken(token);
      this.isAdmin = payload?.role?.toLowerCase() === "admin";
    },

    async fetchTours() {
      try {
        const res = await api.get("/tours/");
        this.tours = res.data;
      } catch (err) {
        console.error("Lỗi fetchTours:", err);
      }
    },

    async addTour() {
      try {
        const res = await api.post("/tours/", this.newTour);
        alert(`✅ Đã thêm tour: ${res.data.name}`);
        this.tours.unshift(res.data);
        this.newTour = {
          name: "",
          location: "",
          description: "",
          price: 0,
          type: "",
          min_people: 1,
          max_people: 10,
          duration_days: 3,
          difficulty: "",
          rating_avg: 0,
          available: true,
        };
      } catch (err) {
        console.error("Lỗi addTour:", err);
        alert(err.response?.data?.detail || "Thêm tour thất bại");
      }
    },

    async deleteTour(id) {
      if (!confirm("Bạn chắc chắn muốn xóa tour này?")) return;
      try {
        await api.delete(`/tours/${id}`);
        this.tours = this.tours.filter((t) => t.id !== id);
        alert("🗑️ Đã xóa tour!");
      } catch (err) {
        console.error("Lỗi deleteTour:", err);
        alert("Không thể xóa tour!");
      }
    },

    prepareEdit(tour) {
      this.editForm = { ...tour };
      this.editingTour = true;
    },

    async saveEdit() {
      try {
        const res = await api.put(`/tours/${this.editForm.id}`, this.editForm);
        const index = this.tours.findIndex((t) => t.id === res.data.id);
        if (index !== -1) this.tours[index] = res.data;
        alert("✅ Cập nhật tour thành công!");
        this.editingTour = false;
      } catch (err) {
        console.error("Lỗi saveEdit:", err);
        alert("Không thể lưu thay đổi!");
      }
    },

    cancelEdit() {
      this.editingTour = false;
      this.editForm = {};
    },
  },
  async mounted() {
    await this.checkAdmin();
    await this.fetchTours();
  },
};
</script>

  /* giữ nguyên toàn bộ CSS cũ của bạn */
<style scoped>
.admin-page {
  padding: 20px;
  max-width: 1100px;
  margin: 0 auto;
  font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.no-access {
  background: #fff7f7;
  border: 1px solid #f8d7da;
  padding: 16px;
  border-radius: 8px;
  color: #842029;
  text-align: center;
  margin-bottom: 16px;
}

/* Form */
.tour-form {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  margin-bottom: 20px;
}
.tour-form h3 {
  margin: 0 0 12px 0;
  color: #0b5fa5;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}
.form-group {
  display: flex;
  flex-direction: column;
}
.form-group label {
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}
.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #d6d6d6;
  font-size: 14px;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0b5fa5;
  box-shadow: 0 0 0 4px rgba(11, 95, 165, 0.08);
}
.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 10px 0;
}
.btn-submit {
  display: inline-block;
  margin-top: 8px;
  background: #0b5fa5;
  color: white;
  border: none;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

/* Table */
.tour-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
}
.tour-table th,
.tour-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #f1f3f5;
  text-align: left;
}
.tour-table th {
  background: #f6fbff;
  color: #0b5fa5;
  font-weight: 700;
}
.tour-table tr:hover {
  background: #fafafa;
}
.active {
  color: #1b7a3a;
  font-weight: 600;
}
.inactive {
  color: #b71c1c;
  font-weight: 600;
}
.action-buttons button {
  margin-right: 6px;
}

/* Popup */
.popup {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(15, 15, 15, 0.45);
}
.popup-content {
  background: white;
  padding: 18px;
  border-radius: 12px;
  width: 520px;
  max-width: 95%;
  box-shadow: 0 10px 30px rgba(2, 6, 23, 0.24);
}
.popup-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 12px;
}
.btn-primary {
  background: #0b5fa5;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
}
.btn-cancel {
  background: #e0e0e0;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
}
</style>
