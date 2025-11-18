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
Ngôn ngữ và framework chính:

- Frontend: Vue.js

- Backend API: Node.js (Express) / Django REST

- Database: MySQL

- Search / Cache: Redis

- AI Module: Python microservice (FastAPI / Flask) sử dụng NLP + Recommender Engine

---

## Công nghệ sử dụng:


 - [![Frontend](https://img.shields.io/badge/Frontend-Vue.js-42B883?style=for-the-badge&logo=vuedotjs&logoColor=white)]()
   - Xây dựng giao diện người dùng trực quan, thân thiện và responsive trên mọi thiết bị.  
   - Hiển thị dữ liệu tour động, tương tác trực tiếp với Backend API.  
   - Tối ưu hiệu suất, tải trang nhanh và dễ bảo trì.



- [![Backend Node.js](https://img.shields.io/badge/Backend-Node.js%20%7C%20Express-339933?style=for-the-badge&logo=node.js&logoColor=white)](#)
   - **Node.js + Express:** xử lý API, quản lý logic nghiệp vụ, kết nối Frontend và Database.  
   - Hỗ trợ mở rộng nhanh, phù hợp hệ thống có nhiều người dùng đồng thời.


- [![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)]()
   - Lưu trữ toàn bộ dữ liệu người dùng, tour, đặt tour, thanh toán.  
   - Hỗ trợ truy vấn nhanh, bảo toàn dữ liệu, phù hợp ứng dụng thực tế.


- [![Redis](https://img.shields.io/badge/Cache%20%2F%20Search-Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)]()
  - Cải thiện tốc độ tìm kiếm tour và phản hồi API nhanh chóng.  
  - Giảm tải truy vấn Database, tối ưu trải nghiệm người dùng.


- [![AI Module](https://img.shields.io/badge/AI%20Module-Python%20%7C%20FastAPI%20%2F%20Flask-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B)]()
   - Phân tích yêu cầu người dùng bằng NLP (Natural Language Processing).  
   - Tích hợp Recommender Engine gợi ý tour phù hợp với sở thích, lịch trình, và ngân sách.  
   - Triển khai dưới dạng microservice, dễ dàng kết nối với Backend.


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

  6. **Các hình ảnh**

<p align = "center"> <img width="848" height="609" alt="image" src="https://github.com/user-attachments/assets/b09a601e-52db-49db-aa11-0ca1671f5c2e" />
 </p>

<p align = "center">Hình 1: Giao diện đăng ký / đăng nhập </p>

<p align = "center"> <img width="848" height="609" alt="image"  src="https://github.com/user-attachments/assets/1ee97d94-80f2-43e9-a227-4327bf7b24e5" />
 </p>
<p align = "center">Hình 2: Giao diện trang chủ </p>

<p align = "center"> <img width="848" height="609" alt="image"  src="https://github.com/user-attachments/assets/d560a712-0987-4278-93ce-007ac530935a" />

 </p>

<p align = "center">Hình 3: Giao diện trang chủ </p>

<p align = "center"> <img width="848" height="609" alt="image"  src="https://github.com/user-attachments/assets/d76e8852-cba5-4f2d-87bf-66e68e74aea2" />

 </p>

<p align = "center">Hình 4: Gia diện Booking </p>

<p align = "center"> <img width="848" height="609" alt="image"  src="https://github.com/user-attachments/assets/075d11e6-6a9d-44bc-8d92-2262aa3f85f3" />

 </p>

<p align = "center">Hình 5: Gia diện thanh toán </p>

<p align = "center"> <img width="848" height="609" alt="image"  src="https://github.com/user-attachments/assets/9895c259-b9bd-4a3a-aa2d-5337a8f10553" />

 </p>

<p align = "center">Hình 6: Gia diện Tour đã đặt </p>

<p align = "center"> <img width="848" height="609" alt="image" src="https://github.com/user-attachments/assets/c01c9284-bc81-43b2-998d-e21e7f7d1e02" />

 </p>

<p align = "center">Hình 7: Gia diện Admin </p>

---

## 📝 4. Các bước cài đặt

🔹 Bước 1: Chuẩn bị môi trường

Node.js & npm (Frontend + Backend Node.js)

Tải Node.js: https://nodejs.org/

Kiểm tra phiên bản:

node -v
npm -v


Phiên bản đề xuất: Node.js >= 16, npm >= 8.

Python (AI Module / Backend Python)

Tải Python 3.10+: https://www.python.org/downloads/

Kiểm tra phiên bản:

python --version
pip --version


MySQL (Database)

Cài đặt MySQL Community Server: https://dev.mysql.com/downloads/mysql/

Tạo cơ sở dữ liệu và user:

CREATE DATABASE tour_db;
CREATE USER 'tour_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON tour_db.* TO 'tour_user'@'localhost';
FLUSH PRIVILEGES;


Docker 

Tải và cài đặt Docker Desktop: https://www.docker.com/products/docker-desktop

🔹 Bước 2: Tải mã nguồn dự án
git clone https://github.com/your-repo/TourBooking-App.git
cd TourBooking-App


Nếu không dùng Git, bấm Download ZIP trên GitHub và giải nén.

🔹 Bước 3: Cài đặt và chạy Frontend
cd frontend
npm install
npm run serve


Truy cập ứng dụng Frontend: http://localhost:8080

Badge công nghệ Frontend:


🔹 Bước 4: Cài đặt và chạy Backend

Node.js Backend:

cd backend
npm install
npm run dev  # hoặc npm start


Python Backend (FastAPI / Flask):

cd backend
pip install -r requirements.txt
uvicorn main:app --reload   # FastAPI
hoặc python app.py  # Flask


Backend chạy mặc định trên cổng 8000: http://localhost:8000

Badge công nghệ Backend:


🔹 Bước 5: Cài đặt và chạy AI Module
cd ai_module
pip install -r requirements.txt
uvicorn ai_app:app --reload


AI Module xử lý NLP + Recommender, nhận yêu cầu từ Frontend và Backend.

Badge công nghệ AI Module:


🔹 Bước 6: Kết nối cơ sở dữ liệu

Cập nhật thông tin kết nối Database trong file config Backend và AI Module:

DB_HOST=localhost
DB_NAME=tour_db
DB_USER=tour_user
DB_PASSWORD=password
DB_PORT=3306


Kiểm tra kết nối bằng cách chạy Backend và truy cập API /health hoặc tạo tour mẫu.

Badge Database:


🔹 Bước 7: Tùy chọn Docker (Container hóa toàn bộ ứng dụng)
docker-compose up --build


Frontend, Backend, AI Module và MySQL sẽ chạy trong container.

Truy cập ứng dụng tại http://localhost:8080

Badge Docker:


🔹 Bước 8: Sử dụng ứng dụng

Mở trình duyệt tại http://localhost:8080.

Tạo tài khoản hoặc đăng nhập.

Tìm kiếm tour, chọn tour muốn đặt.

Nhận gợi ý từ AI và xác nhận đặt tour.

Kiểm tra lịch sử đặt tour và thông tin người dùng.

---

## 👥 5. Liên hệ

👤 Người thực hiện: Đặng Văn Khánh

🏫 Lớp CNTT 16-03 

✉️ Liên hệ qua email: khanh.lehends@gmail.com

📞 Số điện thoại: 0862058018
