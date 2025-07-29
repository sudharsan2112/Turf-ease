import mysql.connector
from datetime import datetime, timedelta

DB_CONFIG = {
        host="db4free.net",
        user="sudharsan",               
        password="sudharsan@sql",    
        database="turfbooking",         
        port=3306
}

def reset_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS slots")

        cursor.execute("""
            CREATE TABLE slots (
                id INT AUTO_INCREMENT PRIMARY KEY,
                slot_date DATE NOT NULL,
                slot_time VARCHAR(50) NOT NULL,
                booked_by VARCHAR(100) DEFAULT NULL
            )
        """)

        today = datetime.today().date()
        for day_offset in range(5):
            date = today + timedelta(days=day_offset)
            for hour in range(16, 23, 2):  
                start = datetime.strptime(f"{hour}:00", "%H:%M")
                end = start + timedelta(hours=2)
                slot = f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"
                cursor.execute("INSERT INTO slots (slot_date, slot_time) VALUES (%s, %s)", (date, slot))

        conn.commit()
        print("Database has been reset and slots re-initialized successfully.")

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    reset_database()
