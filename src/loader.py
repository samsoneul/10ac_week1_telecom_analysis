import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')

database_name = 'telecom'
table_name= 'xdr_data'

connection_params = { "host": "localhost", "user": user, "password": password,
                    "port": "5432", "database": database_name}

engine = create_engine(f"postgresql+psycopg2://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}")

# str or SQLAlchemy Selectable (select or text object)
sql_query = 'SELECT * FROM xdr_data '

df = pd.read_sql(sql_query, con= engine)

print(df.describe())
