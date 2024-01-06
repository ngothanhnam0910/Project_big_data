import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
import pandas as pd
from ntscraper import Nitter

coins_df = pd.read_csv('coin_list.csv')
coins_df['keywords'] = coins_df['keywords'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
coin_codes = coins_df.set_index('coin_codes')['keywords'].to_dict()

class TwitterProducer:
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/logs/producer.log",
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

        self.scraper = Nitter(0)

    def run(self):
        try:
            print("Nhay vao ham run roi")
            self.logger.info("Start running twitter producer...")

            while True:
                try:
                    tweets = self.scraper.get_tweets("coin", mode='hashtag', number=300)
                except Exception as e:
                    self.logger.error(f"Fetching error: {e}")
                    continue

                final_tweets = []
                for x in tweets['tweets']:
                    data = [x['link'], x['text'], x['date']]
                    final_tweets.append(data)

                dat = pd.DataFrame(final_tweets, columns=['link', 'text', 'date'])
                coin_mentions = pd.DataFrame()

                for coin, variants in coin_codes.items():
                    coin_mentions[coin] = dat['text'].str.contains('|'.join(variants), case=False)

                dat['coin_code'] = coin_mentions.apply(lambda row: [coin for coin in coin_codes if row[coin]], axis=1)
                dat = dat.drop(columns=['link'])
                dat = dat[['coin_code', 'text', 'date']]

                for index, row in dat.iterrows():
                    for coin_code in row['coin_code']:
                        tweet_info = f"\"{coin_code}\",\"{row['text']}\",\"{row['date']}\""
                        try:
                            print(tweet_info)
                            self.producer.send('twitterData', bytes(tweet_info, encoding='utf-8'))
                            self.producer.flush()
                        except Exception as e:
                            self.logger.error(f"An error happened while pushing message to Kafka: {e}")
                            continue

        except KafkaError as e:
            self.logger.error(f"An Kafka error happened: {e}")
        except Exception as e:
            self.logger.error(f"An error happened while running the producer: {e}")
        finally:
            self.producer.close()
