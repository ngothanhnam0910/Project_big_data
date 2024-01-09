from cassandra.cluster import Cluster
from datetime import datetime
import json

# Kết nối đến cluster và keyspace
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('coinhub')

# Đọc dữ liệu từ tập tin JSON
with open('./msft2020.json', 'r') as file:
    data = json.load(file)

# Sử dụng câu lệnh INSERT INTO để thêm dữ liệu mới vào bảng coin_data
insert_query = """
   INSERT INTO coin_data (symbol, recorded_time, frequency, high, low, open, close, volume)
   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# Duyệt qua từng dòng dữ liệu và thêm vào bảng
for entry in data:
    date = entry["date"]
    open_price = entry["open"]
    high = entry["high"]
    low = entry["low"]
    close = entry["close"]

    # Chuyển đổi chuỗi ngày thành đối tượng datetime
    recorded_time = datetime.strptime(date, "%Y-%m-%d")

    # Giả sử các giá trị còn lại (symbol, frequency, volume) được giữ nguyên hoặc có giá trị mặc định

    # Thực hiện thêm dữ liệu vào bảng
    session.execute(insert_query, ("BTC", recorded_time, "daily", high, low, open_price, close, 0.0))

# Đóng kết nối
cluster.shutdown()
