# app.py
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col, unix_timestamp
from pyspark.sql.types import DoubleType
import matplotlib.pyplot as plt
import pandas as pd
from pyspark.ml.linalg import DenseVector


spark = SparkSession.builder.appName("CoinPricePrediction").getOrCreate()

file_path = "C:/Users/Admin/OneDrive/Desktop/baitapluutru/Project_big_data/spark/sparkml/output2.csv"
data = spark.read.csv(file_path, header=True, inferSchema=True)
data = data.withColumn("timestamp", unix_timestamp(col("timestamp")).cast(DoubleType()))
data.show()


feature_columns = ["timestamp", "open", "high", "low", "volume"]
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
data_assembled = assembler.transform(data).select("features", "close")

(training_data, test_data, prediction_data) = data_assembled.randomSplit([0.7, 0.2, 0.1], seed=123)

lr = LinearRegression(featuresCol="features", labelCol="close", predictionCol="prediction")
lr_model = lr.fit(training_data)
test_results = lr_model.evaluate(test_data)
print("Root Mean Squared Error (RMSE) on test data: {}".format(test_results.rootMeanSquaredError))

predictions = lr_model.transform(prediction_data)
predictions.show()
predictions_df = predictions.select("features", "close", "prediction").toPandas()
predictions_df["first_feature_value"] = predictions_df["features"].apply(lambda x: x[0].item() if isinstance(x, DenseVector) else None)


plt.figure(figsize=(12, 6))
plt.plot(predictions_df["first_feature_value"], predictions_df["close"], label="Thực tế")
plt.plot(predictions_df["first_feature_value"], predictions_df["prediction"], label="Dự đoán")
plt.title("Biểu đồ Dự đoán và Thực tế của Linear Regression")
plt.xlabel("Timestamp")
plt.ylabel("Giá Bitcoin")
plt.legend()
plt.show()
