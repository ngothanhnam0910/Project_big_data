from cassandra.cluster import Cluster
from datetime import datetime

# Kết nối đến cluster và keyspace
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('coinhub')

# Dữ liệu mới bạn muốn thêm
symbol = 'SNS'
frequency = 'minute'

# Thêm dữ liệu vào bảng coin_data
coin_data_insert_query = """
    INSERT INTO coin_data (symbol, recorded_time, frequency, high, low, open, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
for i in range(100):
    recorded_time = datetime.utcnow()
    high = 50000.0 + i * 100
    low = 49000.0 + i * 100
    open_price = 49500.0 + i * 100
    close_price = 49800.0 + i * 100
    volume = 1000.0 + i * 10
    session.execute(coin_data_insert_query, (symbol, recorded_time, frequency, high, low, open_price, close_price, volume))

# Thêm dữ liệu vào bảng tweet_trending
tweet_trending_insert_query = """
    INSERT INTO tweet_trending (symbol, recorded_time, frequency, count, sentiment)
    VALUES (%s, %s, %s, %s, %s)
"""
for i in range(100):
    recorded_time = datetime.utcnow()
    count = 50 + i * 10
    sentiment = 1
    session.execute(tweet_trending_insert_query, (symbol, recorded_time, frequency, count, sentiment))

# Thêm dữ liệu vào bảng stream_tweet_trending
stream_tweet_trending_insert_query = """
    INSERT INTO stream_tweet_trending (symbol, recorded_time, frequency, count, sentiment)
    VALUES (%s, %s, %s, %s, %s)
"""
for i in range(100):
    recorded_time = datetime.utcnow()
    count = 30 + i * 5
    sentiment = -1
    session.execute(stream_tweet_trending_insert_query, (symbol, recorded_time, frequency, count, sentiment))

# Thêm dữ liệu vào bảng recent_tweet
recent_tweet_insert_query = """
    INSERT INTO recent_tweet (symbol, recorded_time, content)
    VALUES (%s, %s, %s)
"""
for i in range(100):
    recorded_time = datetime.utcnow()
    content = f'This is tweet {i}'
    session.execute(recent_tweet_insert_query, (symbol, recorded_time, content))

# Đóng kết nối
cluster.shutdown()
