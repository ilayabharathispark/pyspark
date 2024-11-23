from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from airflow.operators.dummy import DummyOperator # type: ignore
from airflow.operators.email import EmailOperator  # type: ignore # Import the EmailOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator # type: ignore
from datetime import datetime
from airflow.exceptions import AirflowException # type: ignore



def on_failure_callback(context):
    # Import necessary modules
    from airflow.utils.email import send_email # type: ignore
    
    # Extract relevant information from the context
    task_instance = context['task_instance']
    exception = context['exception']
    dag_run = context['dag_run']
    
    # Prepare email content
    subject = f"Airflow Failure: Task {task_instance.task_id} in DAG {dag_run.dag_id}"
    html_content = f"""
    <h3>Task Failure Details</h3>
    <ul>
        <li><strong>Task ID:</strong> {task_instance.task_id}</li>
        <li><strong>DAG ID:</strong> {dag_run.dag_id}</li>
        <li><strong>Exception:</strong> {exception}</li>
    </ul>
    """
    

    # Send email
    send_email('ilayabharathi334@gmail.com', subject, html_content)

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
    conn_id='spark_e2e',  # Connection ID configured in Airflow
    conf={
        'spark.master': 'spark://spark-master:7077',
        'spark.executor.memory': '2g',
        'spark.driver.memory': '1g',
        'spark.executor.cores': '1',
        'spark.num.executors': '2'
    },
    on_failure_callback=on_failure_callback,
    dag=dag
)

    # End task
end_task = DummyOperator(
        task_id='end',
    )


start_task >> spark_job >> end_task