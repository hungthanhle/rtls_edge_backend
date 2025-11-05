```python
tag_log = []
def log(tag_id, cnt, timestamp):
    tag_log.append((tag_id, cnt, timestamp))
```
# Vấn đề 1
Chọn kiểu dữ liệu là Array cho log khi muốn filter lấy ra log một tag_id thôi thì thực hiện:  
+ Độ phức tạp tìm kiếm: O(n) - phải duyệt qua toàn bộ mảng  
+ Không hiệu quả với dữ liệu lớn  
  
# Vấn đề 2
+ 1 tag_id có nhiều dữ liệu, nhiều dữ liệu không cần thiết (đã bị outdate, nhiều giá trị mà thời gian cách nhau ngắn), hơn hết lại còn append vào memory (biến tag_log)  
+ Sẽ là dư thừa dữ liệu và hiệu năng với yêu cầu chỉ quan tâm tới dữ liệu mới nhất  
  
# Giải pháp:
Vấn đề 1: Lựa chọn kiểu dữ liệu key-value dictionary cho log  
Vấn đề 2: Lựa chọn chỉ ghi log chứ không sử dụng biến (memory), lưu lại dữ liệu vào DB nếu cần thiết  
