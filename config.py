import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="db4free.net",
        user="sudharsan",               
        password="sudharsan@sql",    
        database="turfbooking",         
        port=3306
    )
