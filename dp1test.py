import logging
import azure.functions as func
import requests
import json
import os
import subprocess
import pyodbc


# Got code off of a video
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="dbtest1", methods=["GET"])
def dbtest1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Database connection details
    server = 'weather-db-server.database.windows.net'
    database = 'weather_proj_db'
    username = 'WeatherProjData'  # Replace with your Azure SQL username
    password = 'Wpdta6768'  # Replace with your Azure SQL password
    driver = '{ODBC Driver 18 for SQL Server}'

    # Establish the database connection
    try:
        #conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
        #conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no')
        conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Authentication=SqlPassword;TLSVersion=1.3;")
        cursor = conn.cursor()

        # Execute a test query
        cursor.execute('SELECT TOP 1 * FROM Table1')  # Modify this query as per your table name
        row = cursor.fetchone()
        if row:
            result = f"Row from database: {row}"
        else:
            result = "No data found in test_table."

        # Clean up
        cursor.close()
        conn.close()
        return func.HttpResponse(result, status_code=200)
    except Exception as e:
        logging.error(f"Error while connecting to the database: {e}")
        return func.HttpResponse(
            "Error while connecting to the database.",
            status_code=500
        )