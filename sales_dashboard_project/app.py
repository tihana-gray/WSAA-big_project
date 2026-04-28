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