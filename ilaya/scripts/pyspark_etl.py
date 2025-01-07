from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import datetime

# Create a Spark session
spark = SparkSession.builder \
    .appName("PySpark_ETL") \
    .getOrCreate()


df1=spark.read.option("header","true").csv("/home/ilaya/Downloads/abc.csv")
df2=df1.createOrReplaceTempView("students")
df3=spark.sql("select * from students where date_column >= current_timestamp - INTERVAL '5 MINUTES' AND date_column < current_timestamp").show(truncate=False)
#df3.write.option("header","true").csv("/home/ilaya/Downloads/write/student_performance_data_curated1.csv")

'''Yes, the query will work for your job that runs every 5 minutes. It effectively filters the records based on the date_column to only include those from the last 5 minutes relative to the current timestamp. Here's how it fits into your process:

How the Query Works for Every 5-Minute Job:
Job Execution: When your job runs every 5 minutes, it will execute the SQL query to fetch records that have a date_column value within the last 5 minutes.
Time Frame: Since the job runs at regular intervals (e.g., 12:00, 12:05, 12:10, etc.), each execution will retrieve the relevant records for that specific 5-minute window.
Incremental Data Loading: This allows you to process new data arriving in the table every 5 minutes without duplication.
Example Execution:
If the job runs at 12:00, it will fetch records from 11:55 to 12:00.
If the job runs at 12:05, it will fetch records from 12:00 to 12:05.
'''

