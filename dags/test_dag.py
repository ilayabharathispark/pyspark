from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator  # Import the EmailOperator
from datetime import datetime

# Define a simple function to print the current date
def print_current_date():
    print(f"Current date and time: {datetime.now()}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='jenkins_test_dag',
    default_args=default_args,
    schedule_interval='* * * * *',  # Run every 1 minute
    catchup=False,  # Don't run historical jobs
    tags=['test'],
) as dag:

    # Start task
    start_task = DummyOperator(
        task_id='start',
    )

    # Task to print the current date
    print_date_task = PythonOperator(
        task_id='print_date',
        python_callable=print_current_date,
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

    start_task >> print_date_task >> send_email_task >> end_task
