import mariadb
import sys
import pandas as pd

from dataclasses import dataclass, field
from collections.abc import Iterable
from typing import List


'''
Required Priviledges for user python:
CREATE ON *.*
SELECT, INSERT ON database_name.*
'''


@dataclass
class Database:
    name: str = 'test'
    tables: Iterable = field(init=False)
    user: str = 'python'
    host: str = 'localhost'

    def __post_init__(self, tables=None, columns=None) -> None:
        if tables is None:
            tables = ['zahler', 'readings']

        if columns is None:
            columns = ['(zahler_id int NOT NULL AUTO_INCREMENT KEY,'
                        'zahler_nummer int,'
                        'zahler_name text)',
                       '(reading_id int NOT NULL AUTO_INCREMENT KEY,'
                        'zahler_id int,'
                        'date date,'
                        'entry double)']

        self.tables = zip(tables, columns)
        self.initialize_db()

    def initialize_db(self) -> None:
        '''
        Connects to a MariaDB database on localhost using the
        user 'python' and if it doesn't exist yet creates a database according to the input parameters. Name gives the name of the database, tables a list of table names and column_statement a list of column definitions for those tables.

        '''
        

        try:
            conn = mariadb.connect(
                user=self.user,
                host=self.host)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.name};")
        cur.execute(f"USE {self.name};")

        for table in self.tables:
            sql = f"CREATE TABLE IF NOT EXISTS {table[0]} {table[1]};"
            cur.execute(sql)

        conn.commit()
        conn.close()

    def InsertReading(self, cols: List, values: List, table: str) -> None:
        '''
        Connects to a MariaDB database on localhost using the user "python" and 
        inserts the given values into the columns specified in cols into the table specified by parameter table.
        '''
        try:
            conn = mariadb.connect(
                user=self.user,
                host=self.host)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute(f"USE {self.name};")

        try:
            col_st = ', '.join(cols)
            val_st = ', '.join(values)
            sql = f"INSERT INTO {table} ({col_st}) VALUES ({val_st});"
            cur.execute(sql)
            conn.commit()
            print('done')
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        conn.close()

    def DatabaseToDataFrame(self, cols: List, table_statement: str) -> pd.DataFrame:
        '''
        Connects to a MariaDB database on localhost using the user "python" and
        pulls data specified by the input columns from the database table(s) 
        defined table_statement. 
        Returns the data as a pandas DataFrame.
        '''

        try:
            conn = mariadb.connect(
                user=self.user,
                host=self.host)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute(f"USE {self.name};")

        col_st = ", ".join(cols)
        sql = f"SELECT {col_st} FROM {table_statement};"
        cur.execute(sql)
        df = pd.DataFrame([value for value in cur], columns=cols)

        conn.close()

        return df
