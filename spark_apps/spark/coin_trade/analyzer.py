import os
import logging
import time
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import date_trunc, from_unixtime, col, max, min, sum, first, last, lit
from hdfs import InsecureClient
from logging.handlers import RotatingFileHandler



class CoinTradeDataTransformer():
    def __init__(self):
        self.spark = SparkSession.builder\
            .config("spark.app.name", "CoinTradeDataAnalyzer")\
            .config("spark.master", "yarn")\
            .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0")\
            .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")\
            .config("spark.cassandra.connection.host", "172.20.0.11")\
            .config("spark.cassandra.connection.port", "9042")\
            .config("spark.cassandra.auth.username", "cassandra")\
            .config("spark.cassandra.auth.password", "cassandra")\
            .getOrCreate()

        self.frequency = ['minute', 'hour', 'day', 'week', 'month', 'year']

    def map_time(self, df, frequency):
        return df.withColumn('Trade time', date_trunc(
            frequency, from_unixtime(col('Trade time') / 1000)))

    def analyze_statistics(self, df, frequency):
        df = df.groupBy('Symbol', 'Trade time')\
               .agg(max('Price').alias('high'),
                    min('Price').alias('low'),
                    first('Price').alias('open'),
                    last('Price').alias('close'),
                    sum('Quantity').alias('volume'))
        df = df.select(
            col('Symbol').alias('symbol'),
            col('Trade time').alias('recorded_time'),
            col('close'), lit(frequency).alias('frequency'),
            col('high'), col('low'), col('open'), col('volume'))

        return df

    def transform_data(self, files):
        df = self.spark.read.format('csv')\
            .option('header', True)\
            .option('inferSchema', True)\
            .load(files)
        frequency_dfs = {f: self.map_time(df, f) for f in self.frequency}
        frequency_dfs = {f: self.analyze_statistics(df, f) for f, df in frequency_dfs.items()}
        # This only work because I'm in a hurry. If database to big it will explode
        result_df = self.spark.read.format('org.apache.spark.sql.cassandra')\
            .options(table='coin_data', keyspace='coinhub_2')\
            .load()

        for frequency_df in frequency_dfs.values():
            result_df = result_df.union(frequency_df)\
                .groupBy('symbol', 'recorded_time', 'frequency')\
                .agg(max('high').alias('high'),
                     first('open').alias('open'),
                     last('close').alias('close'),
                     min('low').alias('low'),
                     sum('volume').alias('volume'))
            # Cassandra requires cols in alphabet order
            result_df = result_df.select(['symbol', 'recorded_time', *sorted(result_df.columns[2:])])
        return result_df


    def transform_and_save_data(self, files):
        print('Start transforming data')
        frequency_df = self.transform_data(files)
        frequency_df.write.format('org.apache.spark.sql.cassandra')\
                          .mode('append')\
                          .options(table='coin_data', keyspace='coinhub_2')\
                          .save()


if __name__ == "__main__":
    coinTrade = CoinTradeDataTransformer()
    #list_file = ["coinTradeData_2023-12-21_22-53-57.csv","coinTradeData_2023-12-22_17-46-57.csv", "coinTradeData_2024-01-06_22-53-57.csv"]
    list_file = ["coinTradeData_2023-12-18_13-59-35.csv"]
    list_path_file = ["/opt/spark/data/"+item for item in list_file]
    for path_file in list_path_file:
        coinTrade.transform_and_save_data(path_file)
        print(f"Successful {path_file}")
    # file = "/opt/spark/data/coinTradeData_2023-12-21_22-53-57.csv"
    # coinTrade.transform_and_save_data(file)
    # print("sucessful")