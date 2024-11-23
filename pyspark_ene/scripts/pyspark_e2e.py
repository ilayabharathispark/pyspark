# hello world
import os
import sys
import time
import json
from datetime import datetime
from pyspark.sql import SparkSession        # Import SparkSession from pyspark.sql

# Create a Spark session
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .getOrCreate()

# logger
logger = spark._jvm.org.apache.log4j
logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR) # Set the log level to ERROR



# spark read parquet read
df = spark.read.option("header","true").csv("/home/ilaya/spark_test.csv")
df.createOrReplaceTempView("test")

#df1 = spark parquet read
#

spark.sql("select * from test WHERE NAME = 'ilaya'").show()


# rename columns age to Age
df = df.withColumnRenamed("age","Age")

# d write parquet
df.agg({"Age": "max"}).show()

df.show()



