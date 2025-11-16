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

Đề tài “Ứng dụng công nghệ số trong hệ thống đặt tour du lịch trực tuyến” tập trung vào việc xây dựng một ứng dụng web quản lý tour du lịch, cho phép người dùng tìm kiếm, đặt tour, nhận gợi ý thông minh từ AI và quản lý thông tin cá nhân.

Ứng dụng sử dụng mô hình Frontend – Backend – AI Module – Database, kết hợp công nghệ web hiện đại và trí tuệ nhân tạo để mang đến trải nghiệm thông minh, tiện lợi, và cá nhân hóa.

Người dùng có thể nhập yêu cầu tour bằng câu tự nhiên, AI sẽ phân tích nhu cầu và đưa ra gợi ý tour phù hợp. Backend xử lý logic đặt tour, quản lý thông tin khách hàng và lưu trữ vào cơ sở dữ liệu. Frontend hiển thị giao diện trực quan, thân thiện và hỗ trợ đa thiết bị.

---

## 🔧 2. Ngôn ngữ lập trình sử dụng:
- Frontend: Vue.js

- Backend API: Django REST

- Database: MySQL

- Search / Cache: Redis 

- AI Module: Python microservice (FastAPI / Flask) dùng NLP + Recommender

---

## Công nghệ sử dụng:


 - [![Frontend](https://img.shields.io/badge/Frontend-Vue.js-A7E8BD?style=for-the-badge&logo=vuedotjs&logoColor=1A1A1A)]()  
  - Xây dựng giao diện trực quan, nhẹ và linh hoạt.  
  - Tối ưu tốc độ và dễ học, phù hợp cho các trang tour động.


- [![Backend](https://img.shields.io/badge/Backend%20API-Node.js%20%7C%20Express%20%7C%20Django%20REST%20%7C%20FastAPI-144552?style=for-the-badge&logo=nodedotjs&logoColor=FFFFFF)]()  
  - Xử lý API phía server, quản lý logic nghiệp vụ.  
  - Hỗ trợ cả Node.js và Python framework tùy yêu cầu hệ thống.  


- [![Database](https://img.shields.io/badge/Database-MySQL-FDE5C8?style=for-the-badge&logo=mysql&logoColor=00618A)]()  
  - Lưu trữ dữ liệu tour, người dùng, đặt tour và toàn bộ thông tin của hệ thống.  
  - Hỗ trợ truy vấn nhanh, ổn định, phù hợp hệ thống thực tế.


- [![AI Module](https://img.shields.io/badge/AI%20Module-Python%20%7C%20FastAPI%20%2F%20Flask-A7E8BD?style=for-the-badge&logo=python&logoColor=1A1A1A)]()  
  - Xử lý yêu cầu người dùng bằng NLP (Natural Language Processing).  
  - Tích hợp Recommender Engine gợi ý tour phù hợp.  
  - Triển khai dưới dạng Python microservice (FastAPI / Flask) dễ dàng tích hợp với Backend chính.

---

## 🚀 3. Các chức năng chính và hình ảnh

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
     - “Tour đi biển 3 người 2 ngày 1 đêm ở Nha Trang giá khoảng 20 triêu.”
     - “Tour đi cắm trại 5 người 4 ngày 2 đêm ở Đà Lạt giá khoảng 30 triệu.”
     - “Gợi ý tour Đà Nẵng .”
     - “Gợi ý tour leo núi Hà Giang .”
   - Tự động lọc, phân tích dữ liệu và hiển thị tour hợp lý nhất.
  
Các hình ảnh:

<p align = "center"> <img width="848" height="609" alt="image" src="https://github.com/user-attachments/assets/82aced08-424f-4cd8-9362-aedeea614df3" />
 </p>

<p align = "center">Hình 1: Giao diện thời gian server </p>

<p align = "center"> <img width="848" height="609" alt="image" src="https://github.com/user-attachments/assets/206ec908-e334-448a-bb90-38ab2c1e0daa" />
 </p>
<p align = "center">Hình 2: Giao diện thời gian client </p>

<p align = "center"> <img width="848" height="609" alt="image" src="https://github.com/user-attachments/assets/ed6cd34e-2504-40d8-8477-8d6a1987a454" />
 </p>

<p align = "center">Hình 3: Giao diện chọn múi giờ </p>

<p align = "center"> <img width="848" height="609" alt="image" src="https://github.com/user-attachments/assets/224a6a77-5d3c-403c-8857-80984eecee72" />
 </p>

<p align = "center">Hình 4: Gia diện đồng bộ múi giờ đã chọn </p>

---

## 📝 4. Các bước cài đặt

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

## 👥 5. Liên hệ

👤 Người thực hiện: Đặng Văn Khánh

🏫 Lớp CNTT 16-03 

✉️ Liên hệ qua email: khanh.lehends@gmail.com

📞 Số điện thoại: 0862058018
