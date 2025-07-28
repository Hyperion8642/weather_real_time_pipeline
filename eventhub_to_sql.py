# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(save_to_sql) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import logging
import azure.functions as func
import pyodbc
import os
import json

save_to_sql_blueprint = func.Blueprint()

@save_to_sql_blueprint.event_hub_message_trigger(arg_name="myhub", event_hub_name="weatherstreamingeventhub",
                                                 connection="WeatherAPIFuncEHConnectStr") 
def save_to_sql(azeventhub: func.EventHubEvent):
    logging.info('Triggered by Event Hub')

    try:
        # message = azeventhub.get_body().decode('utf-8')
        data = json.loads(azeventhub.get_body().decode('utf-8'))  # Ensure EventHub is sending JSON

        # SQL connection info from environment vars or app settings
        server = os.environ['weather-db-server.database.windows.net']  # e.g., weather-db-server.database.windows.net
        database = os.environ['weather_proj_db']
        username = os.environ['WeatherProjData']
        password = os.environ['Wpdta6768']
        driver = '{ODBC Driver 18 for SQL Server}'

        conn_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Authentication=SqlPassword;TLSVersion=1.3;"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Flatten any nested fields if needed (e.g. air_quality, alerts, forecast)
        # For now assume top-level flat fields
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO YourTableName ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, values)

        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Data inserted successfully.")

    except Exception as e:
        logging.error(f"Failed to insert data: {e}")
