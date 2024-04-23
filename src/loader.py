import psycopg2
import os

from dotenv import load_dotenv


load_dotenv()

pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')