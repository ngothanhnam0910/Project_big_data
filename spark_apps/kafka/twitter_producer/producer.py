import logging
import os
import pandas as pd
import time
import pytz
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError
from ntscraper import Nitter
from datetime import datetime

def convert_date_to_timestamp(date_str):
    date_format = "%b %d, %Y · %I:%M %p %Z"
    date = datetime.strptime(date_str, date_format)
    date = date.replace(tzinfo=pytz.UTC)
    timestamp = date.timestamp()
    return timestamp

coins_df = pd.read_csv('apps/kafka/coin_producer/symbol_list.csv', header=None)
coin_codes = coins_df[0].tolist()

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
            bootstrap_servers=['host.docker.internal:29092', 'host.docker.internal:29093', 'host.docker.internal:29094'],
            api_version=(0, 11, 5),
            client_id='twitter_producer')

        self.scraper = None

    def run(self):
        try:
            print("Nhay vao ham run roi")
            self.logger.info("Start running twitter producer...")

            self.scraper = Nitter(0)

            while True:
                try:
                    tweets = self.scraper.get_tweets("coin", mode='hashtag', number=200)
                except Exception as e:
                    self.logger.error(f"Fetching error: {e}")
                    time.sleep(300)
                    continue

                final_tweets = []
                for x in tweets['tweets']:
                    data = [x['link'], x['text'], x['date']]
                    final_tweets.append(data)

                dat = pd.DataFrame(final_tweets, columns=['link', 'text', 'date'])
                dat['date'] = dat['date'].apply(convert_date_to_timestamp)

                for coin in coin_codes:
                    dat[coin] = dat['text'].str.contains(coin, case=False)

                dat['coin_code'] = dat.apply(lambda row: [coin for coin in coin_codes if row[coin]], axis=1)
                dat = dat.drop(columns=['link'])
                dat = dat[['coin_code', 'text', 'date']]

                for index, row in dat.iterrows():
                    if not row['coin_code']:
                        continue
                    for coin_code in row['coin_code']:
                        tweet_info = f"\"{coin_code}\",\"{row['text']}\",\"{row['date']}\""
                        try:
                            print(tweet_info)
                            self.producer.send('twitterData', bytes(tweet_info, encoding='utf-8'))
                            print("Successful")
                            self.producer.flush()
                        except Exception as e:
                            self.logger.error(f"An error happened while pushing message to Kafka: {e}")
                            continue

                del tweets
                del final_tweets
                del dat
                time.sleep(60)

        except KafkaError as e:
            self.logger.error(f"An Kafka error happened: {e}")
        except Exception as e:
            self.logger.error(f"An error happened while running the producer: {e}")
            print("After get bug, time sleep")
            time.sleep(300)
            print("Start again")
            self.run()
        finally:
            self.producer.close()