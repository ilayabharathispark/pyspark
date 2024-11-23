from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator  # Import the EmailOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime
from airflow.exceptions import AirflowException



# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='e2e_test',
    default_args=default_args,
    schedule_interval='* * * * *',  # Run every 1 minute
    catchup=False,  # Don't run historical jobs
    tags=['pyspark_e2e'],
) as dag:

    # Start task
    start_task = DummyOperator(
        task_id='start',
    )

 # Configuration for Spark job
spark_job = SparkSubmitOperator(
    task_id='spark_submit_task',
    application='/home/ilaya/pyspark/pyspark_e2e_dag.py',  # Path to your Spark application
    conn_id='your_spark_connection',  # Connection ID configured in Airflow
    conf={
        'spark.master': 'spark://spark-master:7077',
        'spark.executor.memory': '2g',
        'spark.driver.memory': '1g',
        'spark.executor.cores': '1',
        'spark.num.executors': '2'
    },
    dag=dag
)

    # Email task to send email on success
send_email_task = EmailOperator(
        task_id='send_email',
        to='ilayabharathi334@gmail.com',  # Replace with your email address
        subject='DAG Success: {{ task_instance.task_id }}',
        html_content='The print_date task has completed successfully.',
    )

    # End task
end_task = DummyOperator(
        task_id='end',
    )

    # Set task dependencies: start -> print date -> end

start_task >> spark_job >> send_email_task >> end_task


