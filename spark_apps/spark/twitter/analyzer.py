import os
import logging
import time
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import date_trunc, from_unixtime, col, udf, count, sum, lit
from pyspark.sql.types import IntegerType
from hdfs import InsecureClient
from logging.handlers import RotatingFileHandler


positive = [
    "upgrade",
    "upgraded",
    "long",
    "buy",
    "buying",
    "growth",
    "good",
    "gained",
    "well",
    "great",
    "nice",
    "top",
    "support",
    "update",
    "strong",
    "bullish",
    "bull",
    "highs",
    "win",
    "positive",
    "profits",
    "bonus",
    "potential",
    "success",
    "winner",
    "winning",
    "good"]

negative = [
    "downgraded",
    "bears",
    "bear",
    "bearish",
    "drop",
    "volatile",
    "short",
    "sell",
    "selling",
    "forget",
    "down",
    "resistance",
    "sold",
    "sellers",
    "negative",
    "selling",
    "blowout",
    "losses",
    "war",
    "lost",
    "loser"]


class TwitterDataTransformer():
    def __init__(self):
        # Should consider using new image for nodemanager if want to use spark yarn
        # currently mismatching python ver if using udf
        # self.spark = SparkSession.builder\
        #     .config("spark.app.name", "TwitterAnalyzer")\
        #     .config("spark.master", "yarn")\
        #     .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0")\
        #     .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")\
        #     .config("spark.cassandra.connection.host", "172.20.0.11")\
        #     .config("spark.cassandra.connection.port", "9042")\
        #     .config("spark.cassandra.auth.username", "cassandra")\
        #     .config("spark.cassandra.auth.password", "cassandra")\
        #     .getOrCreate()
        self.spark = SparkSession.builder\
            .config("spark.app.name", "TwitterAnalyzer")\
            .config("spark.master", "local[*]")\
            .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0")\
            .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")\
            .config("spark.cassandra.connection.host", "172.20.0.11")\
            .config("spark.cassandra.connection.port", "9042")\
            .config("spark.driver.host", "127.0.0.1")\
            .config("spark.cassandra.auth.username", "cassandra")\
            .config("spark.cassandra.auth.password", "cassandra")\
            .getOrCreate()
        self.frequency = ['minute', 'hour', 'day', 'week', 'month', 'year']

    def map_time(self, df, frequency):
        return df.withColumn('Recorded time', date_trunc(
            frequency, from_unixtime(col('Recorded time'))))

    def analyze_statistics(self, df, frequency):
        def get_sentiment(tweet_content):
            for word in positive:
                if tweet_content.find(word) != -1:
                    return 1
            for word in negative:
                if tweet_content.find(word) != -1:
                    return -1
            return 0

        get_sentiment_udf = udf(lambda content: get_sentiment(content), IntegerType())
        df = df.withColumn('sentiment', get_sentiment_udf(col('Tweet')))
        df = df.groupBy('Symbol', 'Recorded time')\
               .agg(count('Tweet').alias('count'),
                    sum('sentiment').alias('sentiment'))

        df = df.select(col('Symbol').alias('symbol'),
                       col('Recorded time').alias('recorded_time'),
                       col('count'), lit(frequency).alias('frequency'), col('sentiment'))
        return df

    def transform_data(self, files):
        df = self.spark.read.format('csv')\
            .option('mode', 'DROPMALFORMED')\
            .option('header', True)\
            .option('inferSchema', True)\
            .load(files)
        frequency_dfs = {f: self.map_time(df, f) for f in self.frequency}
        frequency_dfs = {f: self.analyze_statistics(df, f) for f, df in frequency_dfs.items()}
     
        result_df = self.spark.read.format('org.apache.spark.sql.cassandra')\
            .options(table='tweet_trending', keyspace='coinhub_2')\
            .load()
        for frequency_df in frequency_dfs.values():
            result_df = result_df.union(frequency_df)\
                .groupBy('symbol', 'recorded_time', 'frequency')\
                .agg(sum('count').alias('count'),
                     sum('sentiment').alias('sentiment'))
            # Cassandra requires cols in alphabet order
            result_df = result_df.select(['symbol', 'recorded_time', *sorted(result_df.columns[2:])])
        return result_df
        # return frequency_dfs


    def transform_and_save_data(self, files):
        print('Start transforming data')
        frequency_df = self.transform_data(files)
        frequency_df = frequency_df.na.drop()

        frequency_df.write.format('org.apache.spark.sql.cassandra')\
                    .mode('append')\
                    .options(table='tweet_trending', keyspace='coinhub_2')\
                    .save()

if __name__ == "__main__":
    
    file =  "/opt/spark/data/test_tweeter.csv"
    twitter =  TwitterDataTransformer()
    # test = twitter.transform_data(file)
    # print(test.show())
    twitter.transform_and_save_data(file)
    print("successful")