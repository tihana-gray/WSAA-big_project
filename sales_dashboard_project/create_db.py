import pandas as pd  # For handling imported CSV data
import sqlite3       # For SQLite databases
import os            # To avoid file reading errors

# File path
file_path = os.path.join("data", "closed_deals_01-01-17-04-2026.csv")
# 📚 References: 
# https://www.geeksforgeeks.org/python/python-os-path-join-method/
# https://docs.python.org/3/library/os.path.html
# https://stackoverflow.com/questions/7132861/how-can-i-create-a-full-path-to-a-file-from-parts-e-g-path-to-the-folder-name

# Loading CSV into DataFrame
df = pd.read_csv(file_path)
# 📚 References:
# https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# https://www.geeksforgeeks.org/pandas/python-read-csv-using-pandas-read_csv/
# https://www.w3schools.com/python/pandas/pandas_csv.asp

# Converting 'Close Date' to datetime format
df['Close Date'] = pd.to_datetime(df['Close Date'], dayfirst=True, errors='coerce')
# 📚 References:
# https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
# https://www.geeksforgeeks.org/pandas/python-pandas-to_datetime/
# https://www.w3schools.com/python/pandas/pandas_cleaning_wrong_format.asp
# https://stackoverflow.com/questions/73595231/pandas-to-datetime-doesnt-work-as-hoped-with-format-d-m-y
# https://github.com/pandas-dev/pandas/issues/25143

# Removing commas and any currency symbols before conversion
df['Amount'] = df['Amount'].astype(str).str.replace(',', '').str.replace('€', '')
# 📚 References:
# https://www.geeksforgeeks.org/pandas/python-pandas-series-str-replace-to-replace-text-in-a-series/
# https://pandas.pydata.org/docs/reference/api/pandas.Series.str.replace.html
# https://stackoverflow.com/questions/57647372/can-you-use-the-pandas-df-str-replace-function-for-multiple-values
# https://stackoverflow.com/questions/39125665/cannot-convert-string-to-float-in-pandas-valueerror

# Converting 'Amount' to numeric format (removing any non-numeric characters)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
# 📚 References:
# https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
# https://www.geeksforgeeks.org/python/python-pandas-to_numeric-method/
# https://www.w3schools.com/python/pandas/pandas_cleaning_wrong_format.asp
# https://stackoverflow.com/questions/78349270/using-pandas-to-number-and-coerce-to-force-values-to-ints-and-still-not-working

# Replacing missing values with 0 
df['Amount'] = df['Amount'].fillna(0)
# 📚 References:
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html
# https://www.geeksforgeeks.org/python/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
# https://www.w3schools.com/python/pandas/ref_df_fillna.asp

# Renaming columns to remove spaces and special characters for SQL compatibility
df.columns = [
    'close_date',
    'deal_name',
    'deal_id',
    'deal_stage',
    'amount',
    'closed_amount',
    'traffic_source'
]
# 📚 References:
# https://medium.com/@analyticsmentor/sql-best-practices-e1c61e96ee27
# https://stackoverflow.com/questions/5461481/formatting-clear-and-readable-sql-queries

# Connecting to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("deals.db")
# 📚 References:
# https://docs.python.org/3/library/sqlite3.html
# https://stackoverflow.com/questions/76571296/how-to-connect-to-sqlite-database-in-python
# https://www.w3schools.com/python/ref_module_sqlite3.asp
# https://www.geeksforgeeks.org/python/python-sqlite-connecting-to-database/

# Adding DataFrame to SQL table named 'deals'
df.to_sql("deals", conn, if_exists="replace", index=False)
# 📚 References:
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
# https://stackoverflow.com/questions/75047288/how-to-use-to-sql-in-pandas

# Closing the database connection
conn.close()
# 📚 References:
# https://stackoverflow.com/questions/3783238/python-database-connection-close
# https://www.geeksforgeeks.org/python/how-to-close-connections-in-psycopg2-using-python/
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.close

print("Database created and data inserted.")

# Previewing first 5 rows
print("First 5 rows of the dataset:")
print(df.head())
# 📚 References:
# https://www.w3schools.com/python/pandas/ref_df_head.asp
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html

# Showing column names
print("Columns in dataset:")
print(df.columns)
# 📚 References:
# https://www.w3schools.com/python/pandas/ref_df_columns.asp
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.columns.html

# Showing basic info about data types and missing values
print("Basic info about data types and missing values:")
print(df.info())
# 📚 References:
# https://www.w3schools.com/python/pandas/ref_df_info.asp
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html


#---------------------------------
# Reading data back from database:
# --------------------------------

# Reconnecting to the database
conn = sqlite3.connect("deals.db")

# Creating cursor to execute SQL queries
cursor = conn.cursor()
# 📚 References:
# https://docs.python.org/3/library/sqlite3.html#cursor-objects
# https://stackoverflow.com/questions/6318126/why-do-you-need-to-create-a-cursor-when-querying-a-sqlite-database
# https://www.geeksforgeeks.org/python/python-sqlite-cursor-object/


