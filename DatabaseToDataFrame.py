import mariadb
import sys
import pandas as pd


def DatabaseToDataFrame(cols, table_statement):
    '''
    INPUT: list, text
    OUTPUT: pandas DataFrame

    Connects to a MariaDB database on localhost using the user "python" and
    pulls data specified by the input columns from table(s) defined in
    table_statement. Returns the data as a pandas DataFrame.
    '''
    try:
        conn = mariadb.connect(
            user="python",
            host="localhost")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()

    SQLstatement = "SELECT " + ", ".join(cols) + " FROM " + table_statement
    cur.execute(SQLstatement)
    df = pd.DataFrame([value for value in cur], columns=cols)

    conn.close()

    return df
