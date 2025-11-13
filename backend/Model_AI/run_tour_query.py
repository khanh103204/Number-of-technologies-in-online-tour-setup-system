import pandas as pd
from nlp_query_parser import parse_query, filter_tours
from recommend import recommend_tours  # hàm gợi ý tour tương tự dựa trên tour_id

def main():
    # 1️⃣ Load dữ liệu tour
    try:
        df = pd.read_csv("backend/Model_AI/data_tour_clean.csv")
    except FileNotFoundError:
        print("⚠ Không tìm thấy file data_tour_clean.csv. Vui lòng kiểm tra đường dẫn.")
        return
    
    # Chuẩn hóa tên cột: loại khoảng trắng + viết thường
    df.rename(columns=lambda x: x.strip().lower(), inplace=True)
    
    # Map các cột cần thiết nếu tên khác
    col_map = {
        'id': 'tour_id',
        'name': 'tour_name',
        'max_people': 'num_people'
    }
    df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)
    
    # Kiểm tra đủ các cột cần thiết
    required_cols = ['tour_id','tour_name','location','type','duration_days','num_people','price']
    for col in required_cols:
        if col not in df.columns:
            print(f"⚠ CSV thiếu cột: {col}. Vui lòng kiểm tra file CSV.")
            return
    
    print("=== Chào mừng bạn đến với hệ thống gợi ý tour tự động ===")
    query = input("Nhập yêu cầu tour của bạn: ")
    
    # 2️⃣ Trích thông tin từ câu hỏi tự nhiên
    criteria = parse_query(query)
    print("\nThông tin trích xuất từ câu hỏi:")
    for k, v in criteria.items():
        print(f"  {k}: {v}")
    
    # 3️⃣ Lọc tour theo tiêu chí
    df_filtered = filter_tours(df, criteria)
    
    if df_filtered.empty:
        print("\n⚠ Không tìm thấy tour nào chính xác theo yêu cầu.")
        return
    
    print("\n✅ Danh sách tour phù hợp:")
    print(df_filtered[required_cols])
    
    # 4️⃣ Gợi ý tour tương tự
    print("\n=== Gợi ý các tour tương tự cho từng tour phù hợp ===")
    for idx, row in df_filtered.iterrows():
        print(f"\nTour: {row['tour_name']} (ID: {row['tour_id']})")
        similar_tours = recommend_tours(row['tour_id'], top_n=5)  # từ recommend.py

        if not similar_tours:
            print("  Không có tour tương tự.")
        else:
            # Nếu recommend_tours trả về DataFrame
            if isinstance(similar_tours, pd.DataFrame):
                similar_tours.rename(columns=lambda x: x.strip().lower(), inplace=True)
                name_col = next((c for c in ['tour_name','name','title'] if c in similar_tours.columns), None)
                sim_col = next((c for c in ['similarity','score'] if c in similar_tours.columns), None)
                if name_col and sim_col:
                    for _, sim_row in similar_tours.iterrows():
                        print(f"  - {sim_row[name_col]} | độ tương đồng: {sim_row[sim_col]:.2f}")
                else:
                    print("  ⚠ Không tìm thấy cột name/similarity trong DataFrame")
            # Nếu recommend_tours trả về list of dict
            elif isinstance(similar_tours, list):
                for sim in similar_tours:
                    name_key = next((k for k in ['tour_name','name','title'] if k in sim), None)
                    sim_key = next((k for k in ['similarity','score'] if k in sim), None)
                    if name_key and sim_key:
                        print(f"  - {sim[name_key]} | độ tương đồng: {sim[sim_key]:.2f}")
                    else:
                        print("  ⚠ Dict trong list không có key name/similarity")
            else:
                print("  ⚠ Kết quả gợi ý tour tương tự không hợp lệ.")

if __name__ == "__main__":
    main()
