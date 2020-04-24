from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

start_time = datetime.now()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_time,
    'email': ['mail@andydang.ca'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
    }

dag = DAG('update_sqlite', default_args=default_args, schedule_interval=timedelta(hours=1))

t1 = BashOperator(
    task_id='call_update',
    bash_command='python /home/andy/covid/backend/db/update.py',
    dag=dag)
