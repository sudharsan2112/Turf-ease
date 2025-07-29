from flask import Flask, render_template, request, redirect, url_for
import model
import qrcode
import base64
from io import BytesIO
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    dates = model.get_dates()
    return render_template('index.html', dates=dates)

@app.route('/slots', methods=['POST'])
def slots():
    selected_date = request.form.get('selected_date')
    slots = model.get_available_slots(selected_date)
    return render_template('slots.html', slots=slots, selected_date=selected_date)

@app.route('/book', methods=['POST'])
def book():
    slot_id = request.form.get('slot_id')
    name = request.form.get('name')
    date = request.form.get('date')

    if model.book_slot(slot_id, name):
        qr_data = f"Slot ID: {slot_id}, Name: {name}, Date: {date}"
        img = qrcode.make(qr_data)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return render_template('result.html', success=True, name=name, date=date, qr_img=qr_img_base64)
    else:
        return render_template('result.html', success=False, name=name, date=date)

@app.route('/admin/reset')
def reset():
    try:
        subprocess.run(['python', 'reset.py'], check=True)
        message = "Database has been reset successfully."
    except subprocess.CalledProcessError:
        message = "Failed to reset the database."
    return render_template("admin.html", message=message)

if __name__ == '__main__':
    app.run(debug=True)