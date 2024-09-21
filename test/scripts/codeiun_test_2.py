from pyspark.sql import SparkSession

# Path to the PostgreSQL JDBC driver JAR
jdbc_driver_path = "/home/ilaya/postgresql-42.2.18.jar"

# Initialize Spark session and include the driver JAR
spark = SparkSession.builder \
    .appName("PostgreSQL Example") \
    .config("spark.jars", jdbc_driver_path) \
    .getOrCreate()

# JDBC connection properties
jdbc_url = "jdbc:postgresql://192.168.1.100:5432/dvdrental"
connection_properties = {
    "user": "postgres",
    "password": "5602",
    "driver": "org.postgresql.Driver"
}

# Read the table into DataFrame
df = spark.read.jdbc(url=jdbc_url, table="customer", properties=connection_properties)

# Show the DataFrame schema
df.printSchema()
