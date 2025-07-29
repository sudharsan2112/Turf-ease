from datetime import datetime, timedelta, date as dt_date
from config import get_connection

def generate_slots():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.today().date()

    for i in range(5):  
        date = today + timedelta(days=i)
        cursor.execute("SELECT COUNT(*) FROM slots WHERE slot_date = %s", (date,))
        if cursor.fetchone()[0] == 0:
            for hour in range(16, 23, 2):  
                start = datetime.strptime(f"{hour}:00", "%H:%M")
                end = start + timedelta(hours=2)
                slot_time = f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"
                cursor.execute("INSERT INTO slots (slot_date, slot_time) VALUES (%s, %s)", (date, slot_time))
    conn.commit()
    conn.close()

def get_dates():
    return [(datetime.today().date() + timedelta(days=i)).isoformat() for i in range(5)]

def get_available_slots(selected_date):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, slot_time FROM slots WHERE slot_date = %s AND booked_by IS NULL"
    cursor.execute(query, (selected_date,))
    all_slots = cursor.fetchall()

    # Filter past time slots if the selected date is today
    if selected_date == dt_date.today().isoformat():
        current_time = datetime.now().time()
        filtered_slots = []
        for slot in all_slots:
            slot_id, slot_time = slot
            start_time_str = slot_time.split(" - ")[0]
            start_time_obj = datetime.strptime(start_time_str, "%I:%M %p").time()
            if start_time_obj > current_time:
                filtered_slots.append(slot)
        slots = filtered_slots
    else:
        slots = all_slots

    conn.close()
    return slots

def book_slot(slot_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE slots SET booked_by = %s WHERE id = %s AND booked_by IS NULL", (name, slot_id))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success
