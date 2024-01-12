
# PROJECT BIGDATA
- Bước 1 : git clone project về máy
- Bước 2: build docker images
  - Chạy lệnh sau:  make build-yarn
- Bước 3: chạy docker-compose file
  - Chạy lệnh:  make run-yarn
- Bước 4: Crawl data và đẩy dữ liệu vào kafka broker (có 2 luồng crawl dữ liêu)
  - B 4.1:  docker exec -it container_name bash
  - B 4.2:  python apps/kafka/coin_producer/producer.py   (crawl data từ Binance và đẩy vào kafka broker với topic là:  coinTradeData)
  - B 4.3:  python apps/kafka/coin_consumer/consumer.py   (Dữ liệu được lấy từ kafka và đẩy vào HDFS)

# Running the code (Spark on Hadoop Yarn cluster)

You can run Spark on the Hadoop Yarn cluster by running:
```shell
make run-yarn
```
or with 2 data nodes:
```shell
make run-yarn-scaled
```
You can submit an example job to test the setup:
```shell
make submit-yarn-test
```
which will submit the `pi.py` example in cluster mode.

You can also submit a custom job:
```shell
make submit-yarn-cluster app=data_analysis_book/chapter03/word_non_null.py
```

There are a number of commands to build the cluster,
you should check the Makefile to see them all. But the
simplest one is:
```shell
make build-yarn
```

## Web UIs
You can access different web UIs. The one I found the most 
useful is the NameNode UI:
```shell
http://localhost:9870
```

Other UIs:
- ResourceManger - `localhost:8088`
- Spark history server - `localhost:18080`

