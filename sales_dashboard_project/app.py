from flask import Flask, jsonify  # Flask for API, jsonify to return JSON
import sqlite3                    # Connecting to SQLite database

# Create Flask app
app = Flask(__name__)

# 📚 References:
# https://flask.palletsprojects.com/en/stable/tutorial/factory/
# https://www.geeksforgeeks.org/python/why-do-we-pass-__name__-to-the-flask-class/
# https://stackoverflow.com/questions/61926327/how-does-app-flask-name-works-exactly-in-a-flask-application

# Connecting to the database
def get_db_connection():
    conn = sqlite3.connect("deals.db")
    conn.row_factory = sqlite3.Row  # Pulls rows as dictionaries instead of tuples, making it easier to work with data
    return conn
# 📚 References:
# https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
# https://zetcode.com/python/sqlite3-connection-row-factory/
# https://stackoverflow.com/questions/44009452/what-is-the-purpose-of-the-row-factory-method-of-an-sqlite3-connection-object
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
# https://www.psycopg.org/psycopg3/docs/api/rows.html


# API route to get all deals
@app.route('/deals', methods=['GET'])
def get_deals():

    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to get all deals
    cursor.execute("SELECT * FROM deals")
    
    rows = cursor.fetchall()

    # Converting rows to list of dictionaries
    deals = [dict(row) for row in rows] 
    # Loop through all rows converting each one to a dictionary and storing them in a list

    conn.close()

    return jsonify(deals)

# 📚 References:
# https://flask.palletsprojects.com/en/stable/quickstart/
# https://www.geeksforgeeks.org/python/flask-app-routing/
# https://www.sitepoint.com/flask-url-routing/
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
# https://www.geeksforgeeks.org/python/use-jsonify-instead-of-json-dumps-in-flask/
# https://www.geeksforgeeks.org/python/how-to-return-a-json-response-from-a-flask-api/
