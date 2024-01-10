import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError
from tweepy import StreamingClient
import os
from ntscraper import Nitter
# import pandas as pd
from datetime import datetime
import time
with open(os.path.abspath(os.getcwd()) + "/apps/kafka/coin_producer/symbol_list.csv") as f:
    symbol_list = f.read().split('\n')
    
class TwitterProducer:
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/apps/kafka/twitter_producer/logs/producer.log",
            maxBytes=104857600, backupCount=10)

        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])

        self.logger = logging.getLogger('twitter_producer')

        self.producer = KafkaProducer(
            bootstrap_servers=['host.docker.internal:29092', 'host.docker.internal:29093'],
            api_version=(0, 11, 5),
            client_id='twitter_producer')
        
        self.scraper = Nitter(0)
        


    def convert_to_unix_timestamp(self, date_string):
        datetime_obj = datetime.strptime(date_string, "%b %d, %Y · %I:%M %p %Z")
        return int(datetime_obj.timestamp())

    def on_response(self, coin_name):
        #  Message from twitter sapi
        # try:
        tweets = self.scraper.get_tweets(coin_name, mode = 'hashtag', number=1000)
        for x in tweets['tweets']:
            tweet_content = x["text"]
            symbol = coin_name
            time_stamp = self.convert_to_unix_timestamp(x["date"])
            tweet_info = f"\"{symbol}\",\"{tweet_content}\", \"{time_stamp}\""
            print(f"tweet_info: {tweet_info}")
            time.sleep(0.1)
            self.producer.send('twitterData', bytes(tweet_info, encoding='utf-8'))
            print(f"Send kafka secessful")
            self.producer.flush()

        # except KafkaError as e:
        #     print(f"An Kafka error happened: {e}")
        # except Exception as e:
        #     print(f"An error happened while pushing message to Kafka: {e}")
        #     exit()

    def run(self):
        print("Start running twitter producer...")
        for i,coin in enumerate(symbol_list):
            try:
                self.on_response(coin)
                time.sleep(15)
            except Exception as e:
                print(f"An error happened while running the producer: {e}")
                print(f"Start sleep 200s")
                time.sleep(60)
                continue
                
if __name__ == "__main__":
    producer = TwitterProducer()
    producer.run()
    