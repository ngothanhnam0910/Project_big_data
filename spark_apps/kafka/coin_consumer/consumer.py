import logging
import os
import tempfile
import datetime
from logging.handlers import RotatingFileHandler
from kafka import KafkaConsumer
from hdfs import InsecureClient


class CoinConsumer:
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/kafka/coin_consumer/logs/consumer.log",
            maxBytes=104857600, backupCount=10)
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])
        self.logger = logging.getLogger('coin_consumer')
        self.consumer = KafkaConsumer(
            'coinTradeData',
            # bootstrap_servers=['localhost:19092', 'localhost:29092', 'localhost:39092'],
            bootstrap_servers=['host.docker.internal:29092', 'host.docker.internal:29093', 'host.docker.internal:29094'],
            group_id='tradeDataConsummers',
            auto_offset_reset='earliest',
            enable_auto_commit=False)
        self.hdfs_client = InsecureClient('http://host.docker.internal:9870', user='root')

    def flush_to_hdfs(self, tmp_file_name):
        current_time = datetime.datetime.now()
        hdfs_filename = "/coinTradeData/" +\
            str(current_time.year) + "/" +\
            str(current_time.month) + "/" +\
            str(current_time.day) + "/"\
            f"coinTradeData.{int(round(current_time.timestamp()))}"

        self.logger.info(
            f"Starting flush file {tmp_file_name} to hdfs")
        flush_status = self.hdfs_client.upload(hdfs_filename, tmp_file_name)
        if flush_status:
            self.logger.info(f"Flush file {tmp_file_name} to hdfs as {hdfs_filename} successfully")
        else:
            raise RuntimeError(f"Failed to flush file {tmp_file_name} to hdfs")
        self.consumer.commit()

    def recreate_tmpfile(self):
        tmp_file = tempfile.NamedTemporaryFile(mode='w+t')
        tmp_file.write('Symbol,Price,Quantity,Trade time\n')
        return tmp_file

    def run(self):
        try:
            tmp_file = self.recreate_tmpfile()
            self.logger.info("Subcribe to topic coinTradeData")
            while True:
                msgs_pack = self.consumer.poll(10.0)
                if msgs_pack is None:
                    continue

                for tp, messages in msgs_pack.items():
                    for message in messages:
                        true_msg = str(message[6])[2: len(str(message[6])) - 1]
                        print(f"true msg: {true_msg}")
                        tmp_file.write(f"{true_msg}\n")

                # File size > 10mb flush to hdfs
                if tmp_file.tell() > 1048576 // 2:
                    self.flush_to_hdfs(tmp_file.name)
                    tmp_file.close()
                    tmp_file = self.recreate_tmpfile()
                    print(f"Thành công")
                    
        except Exception as e:
            self.logger.error(
                f"An error happened while processing messages from kafka: {e}")
            print(f"An error happened while processing messages from kafka: {e}")
        finally:
            tmp_file.close()
            self.consumer.close()
