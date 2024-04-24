import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
import sys
sys.path.append('C:\\Users\\Ourba\\Desktop\\10Academy\\10ac_week1_telecom_analysis\\src')
from loader import load_data
import unittest

class TestLoadData(unittest.TestCase):
    def setUp(self):
        # Load environment variables
        load_dotenv()

        # Get database connection parameters from environment variables
        host = 'localhost'
        port = '5432'
        user = os.getenv('PG_USER')
        password = os.getenv('PG_PASSWORD')
        database_name = 'telecom'
        table_name = 'xdr_data_test'

        # Create test DataFrame
        self.df = pd.DataFrame({
            'id': [1, 2],
            'name': ['test1', 'test2'],
            'age': [25, 30]
        })

        self.engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}")

        with self.engine.connect() as connection:
            # Check if table exists
            table_exists = connection.execute(text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');")).scalar()
            
            # If table does not exist, create it
            if not table_exists:
                create_table_query = connection.execute(text(f"CREATE TABLE {table_name} (id INT PRIMARY KEY, name TEXT, age INT)"))
                connection.commit()

                # Insert test data
                self.df.to_sql(table_name, con=connection, index=False, if_exists='append')

    def test_load_data(self):
        # Call the load_data function
        df_loaded = load_data(
            host='localhost',
            port='5432',
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
            database_name='telecom',
            table_name='xdr_data_test'
        )

        # Verify the loaded DataFrame is not empty
        self.assertFalse(df_loaded.empty, "Loaded DataFrame is empty")
        print("Assertion 1: Loaded DataFrame is not empty")

        # Verify the DataFrame has the expected columns
        expected_columns = ['id', 'name', 'age']
        self.assertListEqual(list(df_loaded.columns), expected_columns, "Unexpected columns in loaded DataFrame")
        print("Assertion 2: DataFrame has the expected columns")

        # Verify the DataFrame has the expected number of rows
        self.assertEqual(len(df_loaded), len(self.df), "Unexpected number of rows in loaded DataFrame")
        print("Assertion 3: DataFrame has the expected number of rows")

        # Verify the data types of the columns
        self.assertTrue(df_loaded['id'].dtype == 'int64', "Unexpected data type for 'id' column")
        self.assertTrue(df_loaded['name'].dtype == 'object', "Unexpected data type for 'name' column")
        self.assertTrue(df_loaded['age'].dtype == 'int64', "Unexpected data type for 'age' column")
        print("Assertion 4: Data types of the columns are as expected")

        # Verify the values in the loaded DataFrame
        self.assertListEqual(list(df_loaded['id']), list(self.df['id']), "Unexpected values in 'id' column")
        self.assertListEqual(list(df_loaded['name']), list(self.df['name']), "Unexpected values in 'name' column")
        self.assertListEqual(list(df_loaded['age']), list(self.df['age']), "Unexpected values in 'age' column")
        print("Assertion 5: Values in the loaded DataFrame are as expected")

    def tearDown(self):
        # Drop test table
        table_name = 'xdr_data_test'
        with self.engine.connect() as connection:
            connection.execute(text(f"DROP TABLE {table_name};"))

if __name__ == "__main__":
    unittest.main()
