import pandas as pd
from sqlalchemy import create_engine

def load_data(host, port, user, password, database_name, table_name):
    connection_params = {
        "host": host,
        "user": user,
        "password": password,
        "port": port,
        "database": database_name
    }

    engine = create_engine(
        f"postgresql+psycopg2://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"
    )

    sql_query = f'SELECT * FROM {table_name}'

    df = pd.read_sql(sql_query, con=engine)
    
    return df
