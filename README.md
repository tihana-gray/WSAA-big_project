# Web Services & Applications Project

## Sales Deals Dashboard (Flask + SQLite + JavaScript)

---

## Overview

This project is a full-stack web application developed as part of the Web Services and Applications module.

It demonstrates how to:

- Process raw CSV data using `Python`
- Store and manage data in a `SQLite` database
- Build a `RESTful API` using `Flask`
- Create a frontend using `HTML`, `CSS`, and `JavaScript`
- Perform full CRUD operations 
- Filter and display data

---

## Project Purpose

The purpose of this Sales Dashboard project is to demonstrate how sales data can be collected, processed, stored, and displayed through a web application.

The project uses a CSV export containing sales deal information, which is cleaned and processed using `Python` and `pandas` before being stored in a `SQLite` database. A `Flask API` is then used to allow interaction with the database through `RESTful` endpoints.

The dashboard frontend allows users to:
- View all won deals
- Add new deals
- Update existing deals
- Delete deals
- Filter deals by traffic source
- Display deal information dynamically in the browser

The project demonstrates practical use of:
- Data cleaning and preparation
- Database creation and management
- REST API development
- CRUD operations
- Frontend and backend integration
- Dynamic JavaScript functionality using Fetch API

---

## Project Structure

sales_dashboard_project/

├── data/
│   └── closed_deals_01-01-17-04-2026.csv
│
├── staticpages/
│   └── index.html
│
├── create_db.py
├── app.py
├── deals.db
├── README.md
└── .gitignore

---

## Technologies Used

- `Python`
- `Flask`
- `SQLite`
- `Pandas`
- `HTML/CSS`
- `JavaScript`

---

## Database Setup (create_db.py)

This script:

- Loads CSV data using `pandas`
- Converts dates to `datetime format`
- Cleans currency values (€ and commas removed)
- Converts amount fields to numeric
- Handles missing values
- Renames columns for SQL compatibility
- Creates SQLite database (`deals.db`)
- Inserts cleaned data into deals table
- Removes "Closed Lost" deals

Run:

python `create_db.py`

---

## Flask API (app.py)

The Flask application provides RESTful endpoints:

### GET all deals

curl http://127.0.0.1:5000/deals

### GET closed won deals

curl http://127.0.0.1:5000/deals/closedwon

### POST new deal

curl -X POST -H "Content-Type: application/json" -d "{\"close_date\":\"2026-05-01\",\"deal_name\":\"Test Deal\",\"deal_id\":123456,\"deal_stage\":\"Closed Won\",\"amount\":1000,\"closed_amount\":0,\"traffic_source\":\"Web\"}" http://127.0.0.1:5000/deals/add

### DELETE deal

curl -X DELETE http://127.0.0.1:5000/deals/delete/123456

### UPDATE deal

curl -X PUT -H "Content-Type: application/json" -d "{\"close_date\":\"2026-05-01\",\"deal_name\":\"Updated Deal\",\"deal_stage\":\"Closed Won\",\"amount\":2000,\"closed_amount\":0,\"traffic_source\":\"Web\"}" http://127.0.0.1:5000/deals/update/123456

---

## Frontend (index.html)

The frontend dashboard allows users to:

- Load all deals
- Add a new deal
- Delete a deal
- Update a deal
- View deal ID, name, and amount
- Filter deals by traffic source using a dropdown

---

## Key Functionality

### Dynamic Data Loading

Uses Fetch API to retrieve and display data from Flask backend.

### Data Cleaning

Ensures numeric values are stored correctly to avoid null values.

### Traffic Source Filtering

Dropdown is populated dynamically from database values and filters results using JavaScript.

### Automatic Dropdown Load

Dropdown loads automatically using `window.onload`.

---

## How to Run

1. Create database

python `create_db.py`

2. Start Flask server

python `app.py`

3. Open browser

http://127.0.0.1:5000

---

## Notes

- Amount must be numeric (no € symbol in input)
- Filtering is handled on frontend
- Database is recreated when script runs

---

## References

Flask
- https://flask.palletsprojects.com

Pandas
- https://pandas.pydata.org/docs

SQLite
- https://docs.python.org/3/library/sqlite3.html

Fetch API
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

JavaScript DOM
- https://developer.mozilla.org/en-US/docs/Web/API/Document

HTML/CSS
- https://www.w3schools.com

**Full list of references is provided with the code.**


## Author

Tihana Gray