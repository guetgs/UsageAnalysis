import mariadb
import sys
import pandas as pd

'''
Required Priviledges for user python:
CREATE ON *.*
SELECT, INSERT ON database_name.*
'''

class Database:
    default_name = 'test'
    default_tables = ('zahler', 'readings')
    default_columns = ('(zahler_id int NOT NULL AUTO_INCREMENT KEY,'
                        'zahler_nummer int,'
                        'zahler_name text)',
                       '(reading_id int NOT NULL AUTO_INCREMENT KEY,'
                        'zahler_id int,'
                        'date date,'
                        'entry double)')

    def __init__(self, name=default_name, 
                 tables=list(default_tables), 
                 column_statements=list(default_columns)):
        '''
        INPUT: text, list, list
        OUTPUT: none

        Connects to a MariaDB database on localhost using the
        user 'python' and if it doesn't exist yet creates a database according to the input parameters. Name gives the name of the database, tables a list of table names and column_statement a list of column definitions for those tables.

        '''
        self.name = name 
        self.tables = zip(tables, column_statements) 
        self.user = 'python' 
        self.host= 'localhost'

        try:
            conn = mariadb.connect(
                user=self.user,
                host=self.host)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS " + self.name + ";")
        cur.execute("USE " + self.name)

        for table in self.tables:
            SQL = ' '.join(['CREATE TABLE IF NOT EXISTS',
                            table[0],
                            table[1],
                            ';'])
            cur.execute(SQL)

        conn.commit()
        conn.close()

    def InsertReading(self, cols, values, table):
        '''
        INPUT: list, list, text
        OUTPUT: None

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
        cur.execute("USE " + self.name)

        try:
            col_statement = "(" + ', '.join(cols) + ")"
            val_statement = "(" + ', '.join(values) + ")"
            fragments = ["INSERT INTO",
                         table,
                         col_statement,
                         "VALUES",
                         val_statement]

            SQLstatement = ' '.join(fragments) + ';'
            cur.execute(SQLstatement)
            conn.commit()
            print('done')
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        conn.close()


    def DatabaseToDataFrame(self, cols, table_statement):
        '''
        INPUT: list, text
        OUTPUT: pandas DataFrame

        Connects to a MariaDB database on localhost using the user "python" and
        pulls data specified by the input columns from the database table(s) 
        defined table_statement. 
        Returns the data as a pandas DataFrame.
        '''
        try:
            conn = mariadb.connect(
                user="python",
                host="localhost")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute("USE " + self.name)

        SQLstatement = "SELECT " + ", ".join(cols) + " FROM " + table_statement
        cur.execute(SQLstatement)
        df = pd.DataFrame([value for value in cur], columns=cols)

        conn.close()

        return df


