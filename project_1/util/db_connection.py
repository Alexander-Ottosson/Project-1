import os

import psycopg2
from psycopg2._psycopg import OperationalError


def create_connection():
    try:
        conn = psycopg2.connect(
            database='trms',
            user=os.environ['database_username'],
            password=os.environ['database_password'],
            host=os.environ['database_host'],
            port=os.environ['database_port']
        )
        return conn
    except OperationalError as e:
        print(f"{e}")
        return None


connection = create_connection()