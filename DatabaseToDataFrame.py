import mariadb
import sys
import pandas as pd
import numpy as np

def DatabaseToDataFrame(cols, table_statement):
	try:
		conn = mariadb.connect(
		user="python",
		host="localhost")
	except mariadb.Error as e:
		print(f"Error connecting to MariaDB Platform: {e}")
		sys.exit(1)
		
	cur = conn.cursor()

	SQLstatement = "SELECT " + ", ".join(cols) +  " FROM " + table_statement
	cur.execute(SQLstatement)
	df = pd.DataFrame([value for value in cur], columns=cols)

	conn.close()

	return df