# Web Services & Applications Project

## Sales Deals Dashboard (Flask + SQLite + JavaScript)

---

## 📝 Overview

This project is a full-stack web application built using Python, Flask, SQLite, HTML, CSS, and JavaScript.

The application processes sales deal data from a CSV file, stores it in a SQLite database, and displays the information through a web dashboard interface.

The project demonstrates:

- CSV data processing using `pandas`
- Database creation and management using `SQLite`
- Backend API development using `Flask`
- Frontend development using `HTML`, `CSS`, and `JavaScript`
- CRUD operations 
- Dynamic filtering using `JavaScript` and `Fetch API`

---

## 💡 Project Purpose

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

## 🏗️ Project Structure

```text
sales_dashboard_project/
│
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
```

---

## ⚙️ Technologies Used

- `Python`
- `Flask`
- `SQLite`
- `Pandas`
- `HTML/CSS`
- `JavaScript`
- `Fetch API`

---

## 📈 Database Setup (create_db.py)

This script:

- Loads CSV data using `pandas`
- Converts dates to `datetime format`
- Cleans currency values (€ and commas removed)
- Converts amount fields to numeric
- Handles missing values with 0
- Renames columns for SQL compatibility
- Creates SQLite database (`deals.db`)
- Inserts cleaned data into `deals` table
- Removes `Closed Lost` deals

Run:

`python` `create_db.py`

---

## 🈸 Flask API (app.py)

The Flask application provides RESTful endpoints:

### GET all deals

`curl http://127.0.0.1:5000/deals`

### GET closed won deals

`curl http://127.0.0.1:5000/deals/closedwon`

### POST new deal

`curl -X POST -H "Content-Type: application/json" -d "{\"close_date\":\"2026-05-01\",\"deal_name\":\"Test Deal\",\"deal_id\":123456,\"deal_stage\":\"Closed Won\",\"amount\":1000,\"closed_amount\":0,\"traffic_source\":\"Web\"}" http://127.0.0.1:5000/deals/add`

### DELETE deal

`curl -X DELETE http://127.0.0.1:5000/deals/delete/123456`

### UPDATE deal

`curl -X PUT -H "Content-Type: application/json" -d "{\"close_date\":\"2026-05-01\",\"deal_name\":\"Updated Deal\",\"deal_stage\":\"Closed Won\",\"amount\":2000,\"closed_amount\":0,\"traffic_source\":\"Web\"}" http://127.0.0.1:5000/deals/update/123456`

---

## 🌐 Frontend (index.html)

The frontend dashboard allows users to:

- Load all won deals from the database
- Add a new deal
- Delete a deal
- Update a deal
- View deal ID, name, and amount
- Filter deals by traffic source using a dropdown

The frontend uses JavaScript Fetch API to communicate with the Flask backend.

---

## 🧠 Key Functionality

### Dynamic Data Loading

Uses Fetch API to retrieve and display data from Flask backend.

### Data Cleaning

The CSV data is cleaned before insertion into the database to prevent formatting and null value issues.

### Traffic Source Filtering

Dropdown is populated dynamically from database values and filters results using JavaScript.

### Automatic Dropdown Load

Dropdown loads automatically using `window.onload`.

---

## 📊 Database Information

The SQLite database file is stored locally as:

`deals.db`

The database is automatically created when:

`python` `create_db.py` is executed.

The database contains one table:

`deals`

Columns:

- close_date
- deal_name
- deal_id
- deal_stage
- amount
- closed_amount
- traffic_source

### Managing the Database

The project database can also be viewed and edited using:

`DB Browser for SQLite`

This allows records inside `deals.db` to be:

- Viewed
- Updated
- Deleted manually
- Queried using SQL

---

## 💻 How to Run

1. Install required libraries

`pip install pandas flask`

2. Create database

python `create_db.py`

3. Start Flask server

python `app.py`

4. Open browser

http://127.0.0.1:5000

---

## 📝 Notes

- Amount must be numeric (no € symbol in input)
- The database is recreated when `create_db.py` runs
- Traffic source filtering is handled on the frontend using JavaScript
- The dashboard communicates with Flask using Fetch API
- Data is stored locally inside `deals.db`

---

## 📚 References

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


⚠️**Full list of references is provided with the code.**


## Author

Tihana Gray