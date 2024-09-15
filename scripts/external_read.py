from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("PySpark Example") \
    .getOrCreate()

df = spark.read.option("header","true").csv("/home/ilaya/spark_test.csv")
df.createOrReplaceTempView("test")
sql_test=spark.sql("select * from test where age > 15")
df.show()
print("===============================================")
sql_test.show()

print("---Read_files_from_HDFS---")

hadoop_read = spark.read.option("header","true").csv("hdfs://localhost:50000/ilaya/spark_test.csv")
hadoop_read.show()

