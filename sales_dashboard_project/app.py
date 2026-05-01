from flask import Flask, jsonify, request  
import sqlite3                 
import os
import webbrowser                 

# Create Flask app
app = Flask(__name__)

# 📚 References:
# https://flask.palletsprojects.com/en/stable/tutorial/factory/
# https://www.geeksforgeeks.org/python/why-do-we-pass-__name__-to-the-flask-class/
# https://stackoverflow.com/questions/61926327/how-does-app-flask-name-works-exactly-in-a-flask-application

# Connecting to the database
def get_db_connection():
    # Get absolute path to this file (app.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Building path to deals.db
    db_path = os.path.join(base_dir, "deals.db")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
# 📚 References:
# https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
# https://zetcode.com/python/sqlite3-connection-row-factory/
# https://stackoverflow.com/questions/44009452/what-is-the-purpose-of-the-row-factory-method-of-an-sqlite3-connection-object
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
# https://www.psycopg.org/psycopg3/docs/api/rows.html
# https://www.geeksforgeeks.org/python/python-os-path-abspath-method-with-example/
# https://stackoverflow.com/questions/38412495/difference-between-os-path-dirnameos-path-abspath-file-and-os-path-dirnam
# https://docs.python.org/3/library/os.path.html


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


# Extracting only 'Close Won' deals
@app.route('/deals/closedwon', methods=['GET'])
def get_closed_won_deals():

    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to filter Closed Won deals only
    cursor.execute("""
    SELECT * FROM deals
    WHERE deal_stage LIKE '%Closed Won%'
    """)

    rows = cursor.fetchall()

    deals = [dict(row) for row in rows]

    conn.close()

    return jsonify(deals)

#------------------
# CREATING NEW DEAL
#------------------

@app.route('/deals/add', methods=['POST'])
def add_deal():

    new_deal = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

# Checking if deal already exists
    cursor.execute("SELECT * FROM deals WHERE deal_id = ?", (new_deal['deal_id'],))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {"error": "Deal already exists"}, 400

    # 📚 References:
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute
    # https://realpython.com/prevent-python-sql-injection/
    # https://stackoverflow.com/questions/775296/mysql-parameterized-queries

    # Inserting deal if it doesn't exist
    cursor.execute("""
    INSERT INTO deals
    (close_date, deal_name, deal_id, deal_stage, amount, closed_amount, traffic_source)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        new_deal['close_date'],
        new_deal['deal_name'],
        new_deal['deal_id'],
        new_deal['deal_stage'],
        new_deal['amount'],
        new_deal['closed_amount'],
        new_deal['traffic_source']
    ))

    conn.commit()
    conn.close()
    
    return {"message": "Deal added successfully"}, 201

    # 📚 References:
        # https://flask.palletsprojects.com/en/latest/api/#flask.request
        # https://www.w3schools.com/sql/sql_insert.asp
        # https://www.geeksforgeeks.org/python/use-jsonify-instead-of-json-dumps-in-flask/
        # https://stackoverflow.com/questions/76701777/posting-json-to-python-api-created-using-flask
        # https://flask.palletsprojects.com/en/stable/api/
        # https://stackoverflow.com/questions/55079926/do-i-need-to-use-methods-get-post-in-app-route
        # https://www.geeksforgeeks.org/python/flask-http-methods-handle-get-post-requests/
        # https://flask.palletsprojects.com/en/stable/quickstart/
        

#------------
# DELETE DEAL
#------------

@app.route('/deals/delete/<int:deal_id>', methods=['DELETE'])
def delete_deal(deal_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM deals WHERE deal_id = ?", (deal_id,))

    conn.commit()
    conn.close()

    return {"message": "Deal deleted successfully"}

# 📚 References:
# https://www.w3schools.com/sql/sql_delete.asp
# https://flask.palletsprojects.com/en/latest/api/#flask.request
# https://stackoverflow.com/questions/61506681/python-flask-delete-request
# https://www.youtube.com/watch?v=7jKsHOZk-IE



if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/deals")
    app.run(debug=True)
# 📚 References:
# https://flask-ptbr.readthedocs.io/en/latest/quickstart.html
# https://www.geeksforgeeks.org/python/how-to-run-a-flask-application/
# https://realpython.com/ref/stdlib/webbrowser/
# https://docs.python.org/3/library/webbrowser.html
# https://www.geeksforgeeks.org/python/python-launch-a-web-browser-using-webbrowser-module/
# https://stackoverflow.com/questions/5916270/pythons-webbrowser-launches-ie-instead-of-default-browser-on-windows-relative
# https://www.w3schools.com/python/ref_module_webbrowser.asp

