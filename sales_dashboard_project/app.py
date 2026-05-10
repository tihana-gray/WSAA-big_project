from flask import Flask, jsonify, request  
from flask import send_from_directory
import sqlite3                 
import os
import webbrowser                 


# -------------------
# CREATING FLASK APP
#--------------------

app = Flask(__name__)

# 📚 References:
# https://flask.palletsprojects.com/en/stable/tutorial/factory/
# https://www.geeksforgeeks.org/python/why-do-we-pass-__name__-to-the-flask-class/
# https://stackoverflow.com/questions/61926327/how-does-app-flask-name-works-exactly-in-a-flask-application
# https://stackoverflow.com/questions/17681762/unable-to-retrieve-files-from-send-from-directory-in-flask
# https://flask.palletsprojects.com/en/stable/api/
# https://tedboy.github.io/flask/generated/flask.send_from_directory.html

# Connecting to the database
def get_db_connection():
    # Get absolute path to this file (app.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Building path to deals.db
    db_path = os.path.join(base_dir, "deals.db")

    # Connection to SQLie database
    conn = sqlite3.connect(db_path)
    
    # Returning rows as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    
    # Returning connection object
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


# --------------
# GET ALL DEALS
#---------------

# Loading index.html: curl http://127.0.0.1:5000/
@app.route('/')
def serve_index():
    return send_from_directory('staticpages', 'index.html') # Sending index.html file from 'staticpages' folder to browser


# curl http://127.0.0.1:5000/deals
@app.route('/deals', methods=['GET'])
def get_deals():

    conn = get_db_connection()  # opens DB connection
    cursor = conn.cursor()      # creates cursor

    # SQL query to get all deals from deals table
    cursor.execute("SELECT * FROM deals")
    
    # Getting all results
    rows = cursor.fetchall()

    # Converting rows to list of dictionaries for JSON formatting
    deals = [dict(row) for row in rows] 

    # Closing connection
    conn.close()

    # Returning data as JSON
    return jsonify(deals)

# 📚 References:
# https://flask.palletsprojects.com/en/stable/quickstart/
# https://www.geeksforgeeks.org/python/flask-app-routing/
# https://www.sitepoint.com/flask-url-routing/
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
# https://www.geeksforgeeks.org/python/use-jsonify-instead-of-json-dumps-in-flask/
# https://www.geeksforgeeks.org/python/how-to-return-a-json-response-from-a-flask-api/


# ----------------------------------
# EXTRACTING 'CLOSED WON' DEALS ONLY
# ----------------------------------

# Only 'Closed Won' deals: curl http://127.0.0.1:5000/deals/closedwon
@app.route('/deals/closedwon', methods=['GET'])
def get_closed_won_deals(): # Filtering deals

    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to filter 'Closed Won' deals only
    cursor.execute("""
    SELECT * FROM deals
    WHERE deal_stage LIKE '%Closed Won%'
    """)

    rows = cursor.fetchall() # Gets filtered results

    deals = [dict(row) for row in rows] # Converting rows to dictionaries

    conn.close()

    return jsonify(deals)

#------------------
# CREATING NEW DEAL
#------------------

# Adding new deal
# curl -X POST -H "Content-Type: application/json" -d "{\"close_date\":\"2026-04-30\",\"deal_name\":\"Test Deal\",\"deal_id\":999999,\"deal_stage\":\"Closed Won\",\"amount\":5000,\"closed_amount\":5000,\"traffic_source\":\"Test\"}" http://127.0.0.1:5000/deals/add
@app.route('/deals/add', methods=['POST'])
def add_deal(): # Function to insert a deal

    # JSON data gets sent in the request body
    new_deal = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Checking if deal already exists
    cursor.execute("SELECT * FROM deals WHERE deal_id = ?", (new_deal['deal_id'],))
    existing = cursor.fetchone() # Giving results for the above

    # If deal already exists this part returns error response
    if existing:
        conn.close()
        return {"error": "Deal already exists"}, 400

    # 📚 References:
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute
    # https://realpython.com/prevent-python-sql-injection/
    # https://stackoverflow.com/questions/775296/mysql-parameterized-queries


    # Inserting deal in the database if it doesn't exist
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

# Delete deal:  curl -X DELETE http://127.0.0.1:5000/deals/delete/999999
@app.route('/deals/delete/<int:deal_id>', methods=['DELETE'])
def delete_deal(deal_id): # Taking deal_id from URL

    conn = get_db_connection()
    cursor = conn.cursor()

    # Deleting specific deal based on deal_id
    cursor.execute("DELETE FROM deals WHERE deal_id = ?", (deal_id,))

    conn.commit()
    conn.close()

    return {"message": "Deal deleted successfully"}

# 📚 References:
# https://www.w3schools.com/sql/sql_delete.asp
# https://flask.palletsprojects.com/en/latest/api/#flask.request
# https://stackoverflow.com/questions/61506681/python-flask-delete-request
# https://www.youtube.com/watch?v=7jKsHOZk-IE


#-------------
# UPDATE DEAL
#-------------

# curl -X PUT -H "Content-Type: application/json" -d "{\"close_date\":\"2026-05-01\",\"deal_name\":\"Updated Deal\",\"deal_stage\":\"Closed Won\",\"amount\":6000,\"closed_amount\":6000,\"traffic_source\":\"Updated\"}" http://127.0.0.1:5000/deals/update/999999
@app.route('/deals/update/<int:deal_id>', methods=['PUT']) # Route for updating
def update_deal(deal_id):  # Getting deal_id from URL

    # Getting updated data from request
    updated_data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Updating existing deal with parameterised SQL query
    cursor.execute("""
UPDATE deals
SET close_date = ?,
    deal_name = ?,
    deal_stage = ?,
    amount = ?,
    closed_amount = ?,
    traffic_source = ?
WHERE deal_id = ?                                               
""", (
    updated_data['close_date'],
    updated_data['deal_name'],
    updated_data['deal_stage'],
    updated_data['amount'],
    updated_data['closed_amount'],
    updated_data['traffic_source'],
    deal_id 
))
    # Without WHERE clause all records would be updated

    # Checking if anything was updated (if no rows updated 'deal not found')
    if cursor.rowcount == 0:
        conn.close()
        return {"error": "Deal not found"}, 404

    conn.commit()
    conn.close()

    return {"message": "Deal updated successfully"} # If succesful


# 📚 References:
# https://www.w3schools.com/sql/sql_parameterized_queries.asp
# https://explore-flask.readthedocs.io/en/latest/views.html
# https://www.w3schools.com/python/python_mysql_update.asp
# https://www.psycopg.org/docs/cursor.html
# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-rowcount.html
# https://stackoverflow.com/questions/51657427/python-mysql-using-cursor-rowcount-before-and-after-inserting-a-row
# https://iamjeremie.me/post/2025-02/parsing-json-payload-on-rest-api-call-with-flask/
# https://codesignal.com/learn/courses/mastering-flask-http-methods/lessons/updating-data-with-put-requests
# https://medium.com/@obotnt/understanding-the-difference-between-get-json-and-request-json-in-flask-d612d1fbc895
# https://www.w3schools.com/sql/sql_parameterized_queries.asp
# https://stackoverflow.com/questions/4712037/what-is-parameterized-query
# https://www.psycopg.org/psycopg3/docs/basic/params.html
# https://stackoverflow.com/questions/775296/mysql-parameterized-queries


# Running application
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
    
# 📚 References:
# https://flask-ptbr.readthedocs.io/en/latest/quickstart.html
# https://www.geeksforgeeks.org/python/how-to-run-a-flask-application/
# https://realpython.com/ref/stdlib/webbrowser/
# https://docs.python.org/3/library/webbrowser.html
# https://www.geeksforgeeks.org/python/python-launch-a-web-browser-using-webbrowser-module/
# https://stackoverflow.com/questions/5916270/pythons-webbrowser-launches-ie-instead-of-default-browser-on-windows-relative
# https://www.w3schools.com/python/ref_module_webbrowser.asp

