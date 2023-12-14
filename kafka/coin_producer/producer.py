import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient
import os


class CoinProducer:
    def __init__(self):
        log_handler = RotatingFileHandler(
     
            f"{os.path.abspath(os.getcwd())}/kafka/coin_producer/logs/producer.log",
            maxBytes=104857600, backupCount=10)
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])
        self.logger = logging.getLogger('coin_producer')

        self.producer = KafkaProducer(
            # security_protocol="SSL",
            bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
            # bootstrap_servers=['localhost:29092','localhost:29093','localhost:29094'],
            api_version=(0, 11, 5),
            client_id='coin_producer'
        )

    def message_handler(self, message):
        #  Message from binance sapi
        try:
            if(len(message.keys()) == 11):
                trade_info = f"{message['s']},{message['p']},{message['q']},{message['T']}"
                print(f"trade_info: {trade_info}")
                self.producer.send('coinTradeData', bytes(trade_info, encoding='utf-8'))
                print("Send to kafka sucessfull")
                self.producer.flush()
        except KafkaError as e:
            self.logger.error(f"An Kafka error happened: {e}")
            print(f"An Kafka error happened :  {e}")
        except Exception as e:
            self.logger.error(f"An error happened while pushing message to Kafka: {e}")
            print(f"Exception error")

    def crawl_from_binance(self, symbol_list):
        try:
            ws_client = WebsocketClient()
            self.logger.info("Start running coin producer...")
            print(f"Start running coin producer")
            ws_client.start()
            for idx, symbol in enumerate(symbol_list):
                ws_client.trade(symbol, idx + 1, self.message_handler)
            while True:
                pass
        except Exception as e:
            self.logger.error(f"An error happened while streaming: {e}")
        finally:
            ws_client.stop()

    def run(self):
        with open(os.path.abspath(os.getcwd()) + "/kafka/coin_producer/symbol_list.csv") as f:
            symbol_list = f.read().split('\n')
        self.crawl_from_binance(symbol_list)

if __name__ == "__main__":
    coin_producer = CoinProducer()
    coin_producer.run()