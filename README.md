# CoinHub

## Bước 1:
- Clone repo từ github về từ nhánh master
- Yều cầu: 
    - Đã có anaconda để tạo môi trường
    - Đã có docker và docker-compose (cài docker-destop để dễ quản lý log)

## Bước 2:
- Checkout ra 1 nhánh riêng : git checkout branch_name
- Tạo 1 môi trường mới
    - conda create --name mt_name python=3.7
    - pip install -r requirement.txt
    - conda activate mt_name
## Bước 3:
- Để khởi tạo cụm kafka: docker-compose up -d
- Để khởi tạo cụm hadoop: 
    - cd hadoop
    - docker network create hadoop_network
    - docker build -t hadoop-base:3.3.1 -f Dockerfile .
    - docker-compose -f docker-compose-hadoop.yml up -d

## Bước 4:
- Để crawl dữ liệu coin:
    - python kafka/coin_producer/app.py: để đẩy message từ producer vào kafka broker
    - python kafka/coin_consumer/app.py: Lưu file về local file (đặt ten theo thoi gian tao file)
