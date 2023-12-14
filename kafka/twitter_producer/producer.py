import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError
from tweepy import StreamingClient, StreamRule
import os

with open(os.path.abspath(os.getcwd()) + "/kafka/coin_producer/symbol_list.csv") as f:
    symbol_list = f.read().split('\n')

# This only need to do once
twitter_filter = [
    StreamRule('#' + ' OR #'.join(symbol_list[:33]), 'coins 1-33'),
    StreamRule('#' + ' OR #'.join(symbol_list[33:67]), 'coins 34-67'),
    StreamRule('#' + ' OR #'.join(symbol_list[67:100]), 'coins 68-100'),
    StreamRule('#btcusdt', 'abc')
]


class TwitterProducer(StreamingClient):
    def __init__(self, bearer_token, return_type=dict, **kwargs):
        super().__init__(bearer_token=bearer_token, return_type=return_type)
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/kafka/twitter_producer/logs/producer.log",
            maxBytes=104857600, backupCount=10)
        
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])
        
        self.logger = logging.getLogger('twitter_producer')
        
        self.producer = KafkaProducer(
            bootstrap_servers=['127.0.0.1:9092','127.0.0.1:9093','127.0.0.1:9094'],
            api_version=(0, 11, 5),
            client_id='twitter_producer')

        self.add_rules(twitter_filter)

    def on_response(self, response):
        #  Message from twitter sapi
        try:
            self.logger.info("Received response: %s", response)
            tweet_content = response.data['text']
            symbol = None
            for base_symbol in symbol_list:
                if str(tweet_content).lower().find('#' + base_symbol) != -1:
                    symbol = base_symbol
                    break
            tweet_info = f"\"{symbol}\",\"{tweet_content}\""

            if symbol:
                print(f"tweet_info: {tweet_info}")
                self.producer.send('twitterData', bytes(tweet_info, encoding='utf-8'))
                self.producer.flush()
        except KafkaError as e:
            self.logger.error(f"An Kafka error happened: {e}")
        except Exception as e:
            self.logger.error(f"An error happened while pushing message to Kafka: {e}")

    def run(self):
        try:
            print("Nhay vao ham run roi")
            self.logger.info("Start running twitter producer...")
            self.filter()
            print(f"Qua ham filter")
            while True:
                pass
        except Exception as e:
            self.logger.error(f"An error happened while streaming: {e}")
        finally:
            self.disconnect()
