# 1. Thiết lập môi trường và phương pháp thực thi
0. Set up
Install Dependency
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Initialize DB
```
python db.py
```
1. Chạy Tag Simulator
```
python tag_simulator.py
```
2. Chạy Server tiếp nhận
```
python main.py
```
  
# 2. Giải thích phương thức giả lập (simulation) Tag
## 2.1. Dữ liệu
Chọn kiểu dữ liệu dict cho giá trị tag trong giả lập, mô tả như dưới đây:  
```
{
    tag_value: tag_count,
}
```
Ví dụ:  
```
{
    "fa451f0755d8": 197,
    "ab234c9981ff": 52,
    "cd998ab77ef1": 310
}
```
Giúp:  
Tra cứu nhanh (O(1)), Cập nhật đơn giản  
Hiệu quả bộ nhớ  
## 2.2. Truyền dữ liệu
Phần tạo giá trị giả lập, thực hiện thay đổi cnt mỗi 2 giây  
Đã thực hiện log "TAG,{tag_id},{self.tags[tag_id]},{timestamp}"  
Để thực hiện truyền log:  
+ Tạo một server websocket ws://localhost:5000  
+ Khi start server kiểm tra server_socket connection, nếu có connection thực hiện tạo thread với connection rồi set up self.client_socket  
+ Tạo một thread generate data như mô tả phía trên, khi có client_socket thực hiện gửi dữ liệu là log  
## 2.3. Nhận dữ liệu  
+ client tạo connect tới ws://localhost:5000  
+ Set up giá trị tag  
```
{
    tag_value: tag_count,
}
```
+ Nhận và xử lý log, lấy ra giá trị: tag_id, count, timestamp. Qua đó kiểm tra sự thay đổi của count và thực hiện các yêu cầu như lưu, ... .  
  
# 3. Ví dụ về phương pháp kiểm thử (test) API (ví dụ: lệnh curl)  
3. Chạy API Server (FastAPI)  
```
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```
## 3.1. Tra cứu toàn bộ (Get all tags)  
```
curl http://localhost:8000/tags
```
## 3.2. Tra cứu chi tiết (Get tag by id)  
```
curl http://localhost:8000/tag/fa451f0755d8
```
## 3.3. Đăng ký (Register new tag)  
```
curl -X POST http://localhost:8000/tags -H "Content-Type: application/json" -d '{"id": "fa451f0755d9", "description": "Helmet Tag for worker fa451f0755d9"}'
```
