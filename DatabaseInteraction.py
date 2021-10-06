import mariadb
import sys
import pandas as pd


def DatabaseToDataFrame(cols, table_statement, database):
    '''
    INPUT: list, text, text
    OUTPUT: pandas DataFrame

    Connects to a MariaDB database on localhost using the user "python" and
    pulls data specified by the input columns from the database table(s) 
    defined in database and table_statement. 
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
    cur.execute("USE " + database)

    SQLstatement = "SELECT " + ", ".join(cols) + " FROM " + table_statement
    cur.execute(SQLstatement)
    df = pd.DataFrame([value for value in cur], columns=cols)

    conn.close()

    return df


def InsertReading(cols, values, table, database):
    '''
    INPUT: list, list, text
    OUTPUT: None

    Connects to a MariaDB database on localhost using the user "python" and 
    inserts the given values into the columns specified in cols.
    '''
    try:
        conn = mariadb.connect(
            user="python",
            host="localhost")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()
    cur.execute("USE " + database)

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