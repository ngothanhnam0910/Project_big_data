import logging
import os
import tempfile
from datetime import datetime
from logging.handlers import RotatingFileHandler
from kafka import KafkaConsumer
from hdfs import InsecureClient
# import pydoop.hdfs as hdfs

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
            bootstrap_servers=['127.0.0.1:9092','127.0.0.1:9093','127.0.0.1:9094'],
            group_id='tradeDataConsummers',
            auto_offset_reset='earliest',
            enable_auto_commit=False)
        # self.hdfs_client = InsecureClient('127.0.0.1:9870', user='root')

    def create_file_name(self):
        now = datetime.now()
        file_name = f"coinTradeData_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

        return f"hadoop/data/coin/{file_name}"

    def write_to_txt(self, data, file_name):
        #file_name = f"hadoop/data/coin/{file_name}"
        with open(file_name, mode='a') as file:
            file.write(data)

    def run(self):
        try:
            self.logger.info("Subcribe to topic coinTradeData")
            file_name = self.create_file_name()
            # print(file_name)
            # exit()
            while True:
                msgs_pack = self.consumer.poll(10.0)
                if msgs_pack is None:
                    continue                
                
                for tp, messages in msgs_pack.items():
                    for message in messages:
                        true_msg = str(message[6])[2: len(str(message[6])) - 1]

                        # write to file
                        self.write_to_txt(f"{true_msg}\n", file_name)
                        
                        # check size of file
                        file_size = os.path.getsize(file_name) if os.path.exists(file_name) else 0
                        print(f"file_size: {file_size}")
                        if file_size >= 1024 * 1024 * 512 : # size > 512 MB
                            file_name = self.create_file_name() 
                        print(f"write succes {true_msg}")
                        
        except Exception as e:
            self.logger.error(
                f"An error happened while processing messages from kafka: {e}")
            print(f"error: {e}")
        finally:
            # tmp_file.close()
            self.consumer.close()
