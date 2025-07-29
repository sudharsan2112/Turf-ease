import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sudharsan@sql1121",  
        database="turf_booking"
    )
