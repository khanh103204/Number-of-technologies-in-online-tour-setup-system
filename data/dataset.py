import mysql.connector
import csv

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'travel_db'
}

conn = None
cursor = None

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True)
    
    cursor.execute("SELECT * FROM tours")
    
    columns = [desc[0] for desc in cursor.description]
    
    # Lưu CSV chuẩn UTF-8 với BOM, Excel sẽ đọc đúng tiếng Việt
    with open('tours_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(columns)               # ghi header
        writer.writerows(cursor.fetchall())    # ghi dữ liệu
    
    print("Xuất CSV thành công, định dạng chuẩn!")

except mysql.connector.Error as err:
    print("Lỗi kết nối hoặc truy vấn:", err)

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
