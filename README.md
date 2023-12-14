# CoinHub

## Bước 1:
- Clone repo từ github về từ nhánh master
- Đã có anaconda trên máy (ko có thì cài đặt về máy local)
## Bước 2:
- Checkout ra 1 nhánh riêng : git checkout branch_name
- Tạo 1 môi trường và install thư viện trong file requirement.txt  : pip install -r requirement.txt
- Sau đó activate vào môi trường 
## Bước 3:
- Step1: docker-compose up -d  (run cụm kafka)
- Step2: Mở 1 terminal mới và chạy lệnh:  docker-compose up -d (khởi động cụm hadoop)
## Bước 4:
- python kafka/coin_producer/app.py: để đẩy message từ producer vào kafka broker
- python kafka/coin_consumer/app.py: push dữ liệu từ broker tới consumer(hdfs)
