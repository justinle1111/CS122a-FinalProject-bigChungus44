# db/connection.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="test",
        password="password",
        database="CS122a"
    )
