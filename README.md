<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
   ỨNG DỤNG CÔNG NGHỆ SỐ TRONG HỆ THỐNG ĐẶT TOUR DU LỊCH TRỰC TUYẾN 
</h2>

<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
        <img src="docs/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---

## 📘 1. Giới thiệu hệ thống

**SMARTTOUR_AI** là ứng dụng công nghệ số hỗ trợ **đặt tour du lịch trực tuyến thông minh**, được xây dựng bằng **Flutter (Material 3, Riverpod)**.  
Ứng dụng giúp khách hàng tìm kiếm, gợi ý và đặt tour nhanh chóng, đồng thời cho phép quản trị viên và nhà cung cấp quản lý tour, khách hàng, lịch trình và doanh thu.  
Tích hợp **AI trợ lý du lịch** giúp người dùng tìm tour phù hợp với nhu cầu cá nhân chỉ bằng ngôn ngữ tự nhiên.

---

### ⚙️ Thành phần hệ thống

- **Người dùng (Khách du lịch):**
  - Đăng ký / Đăng nhập tài khoản.
  - Tìm kiếm tour theo điểm đến, giá, thời gian, loại hình.
  - Nhận **gợi ý tour từ AI** dựa trên sở thích, lịch sử tìm kiếm.
  - Đặt tour, thanh toán, và theo dõi đơn đặt.

- **Quản trị viên / Nhà cung cấp:**
  - Thêm, sửa, xóa thông tin tour.
  - Quản lý danh mục tour, loại hình du lịch, giá vé.
  - Xem thống kê lượt đặt tour, doanh thu và đánh giá.

- **Trợ lý AI (AI Travel Agent):**
  - Phân tích nhu cầu người dùng và gợi ý tour phù hợp.
  - Có thể trả lời câu hỏi như:
    - “Tôi muốn đi du lịch Đà Lạt 3 ngày 2 đêm, gợi ý tour giúp tôi.”
    - “Có tour nào dưới 3 triệu không?”
    - “Tôi muốn du lịch biển trong tháng tới.”
  - Tích hợp mô hình **Ollama Llama3.2 / GPT local gateway** qua mạng nội bộ.
  - Hỗ trợ cả **trò chuyện tự nhiên và hành động đặt tour trực tiếp.**

---

## 🧩 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
|-------------|------------|
| **Ngôn ngữ** | Dart |
| **Framework** | Flutter (Material 3) |
| **State Management** | Riverpod |
| **CSDL nội bộ** | SharedPreferences / Hive |
| **AI Integration** | OpenAI / Ollama Local Gateway |
| **Kiến trúc** | MVVM (Models – State – Features – Widgets) |
| **Giao diện** | Material 3, Dark/Light mode tự động |

---

## 🚀 3. Các chức năng chính

1. **Đăng ký / Đăng nhập**
   - Hỗ trợ đăng nhập bằng email hoặc số điện thoại.
   - Lưu tài khoản cục bộ (offline-first).
   - Phân quyền **User / Admin / Provider**.

2. **Tìm kiếm & gợi ý tour**
   - Tìm tour theo tên, địa điểm, giá, loại hình.
   - AI gợi ý tour theo thói quen, thời gian và sở thích.
   - Hiển thị danh sách tour nổi bật, khuyến mãi, mới nhất.

3. **Đặt tour & thanh toán**
   - Chọn tour, nhập thông tin hành khách.
   - Tùy chọn thanh toán online/offline.
   - Xác nhận và gửi vé điện tử.

4. **Quản lý tour (Admin/Provider)**
   - Thêm mới, cập nhật, ẩn/hiện tour.
   - Xem thống kê lượt đặt, doanh thu theo tháng.
   - Quản lý danh mục điểm đến, loại tour, phương tiện.

5. **AI Trợ lý du lịch**
   - Gợi ý tour phù hợp theo yêu cầu tự nhiên:
     - “Tour 2 ngày 1 đêm ở miền Trung.”
     - “Gợi ý tour Đà Nẵng vào dịp Tết.”
   - Tự động lọc, phân tích dữ liệu và hiển thị tour hợp lý nhất.

---

## 🧠 4. Giao diện ứng dụng

<p align="center">
  <img src="<img width="1916" height="902" alt="image" src="https://github.com/user-attachments/assets/20df75b8-1b2e-4e9f-a906-9e2e3a5d9c02" /> width="400"/>
</p>
<p align="center"><em>Trang chủ – gợi ý tour thông minh</em></p>

<p align="center">
  <img src="docs/screens/2_search.jpg" width="400"/>
</p>
<p align="center"><em>Tìm kiếm và lọc tour theo tiêu chí</em></p>

<p align="center">
  <img src="docs/screens/3_booking.jpg" width="400"/>
</p>
<p align="center"><em>Đặt tour và thanh toán nhanh chóng</em></p>

<p align="center">
  <img src="docs/screens/4_admin.jpg" width="400"/>
</p>
<p align="center"><em>Giao diện quản trị và thống kê</em></p>

---

## ⚙️ 5. Hướng dẫn cài đặt và chạy ứng dụng

### 🔧 Yêu cầu hệ thống

- **Flutter SDK:** >= 3.22  
- **Dart SDK:** >= 3.3  
- **Thiết bị:** Android 8+ / iOS 14+  
- **Dung lượng:** ~60MB  
- **Mạng:** Có thể hoạt động offline (AI yêu cầu kết nối mạng nội bộ khi bật gateway).

---

### ⚙️ Các bước cài đặt và chạy

1. **Clone mã nguồn:**
   ```bash
   git clone https://github.com/khanh103204/Number-of-technologies-in-online-tour-setup-system.git
   cd smarttour_ai
