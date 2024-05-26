from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Listas de veterinários e horários disponíveis
veterinarians = ["Dr. João Silva", "Dra. Maria Fernandes", "Dr. Carlos Alberto", "Dra. Ana Paula"]
veterinarian_home_visit = ["Dra. Maria Fernandes", "Dra. Ana Paula"]
available_times = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]

appointments = []

# Nome do arquivo JSON para salvar as consultas e usuários
APPOINTMENTS_FILE = 'appointments.json'
USERS_FILE = 'users.json'

def load_appointments():
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_appointments():
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump(appointments, f, default=str)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, default=str)

def is_time_available(vet_name, date_time):
    for appointment in appointments:
        if appointment['vet_name'] == vet_name and appointment['date_time'] == date_time:
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if any(user['username'] == username for user in users):
            flash('Username already exists.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        users.append({'username': username, 'password': hashed_password})
        save_users(users)
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        user = next((user for user in users if user['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if 'username' not in session:
        flash('Please log in to schedule an appointment.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        pet_name = request.form['pet_name']
        owner_name = request.form['owner_name']
        vet_name = request.form['vet_name']
        home_visit = request.form.get('home_visit') == 'on'
        date_str = request.form['date']
        time_str = request.form['time']
        address = request.form['address']
        phone_number = request.form['phone_number']
        date_time_str = f"{date_str} {time_str}"
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

        if is_time_available(vet_name, date_time_str):
            new_appointment = {
                'username': session['username'],
                'pet_name': pet_name,
                'owner_name': owner_name,
                'vet_name': vet_name,
                'home_visit': home_visit,
                'date_time': date_time_str,
                'address': address,
                'phone_number': phone_number
            }
            appointments.append(new_appointment)
            save_appointments()
            return redirect(url_for('view_appointments'))
        else:
            return render_template('schedule.html', veterinarians=veterinarians, veterinarian_home_visit=veterinarian_home_visit, available_times=available_times, error="Horário indisponível para o veterinário selecionado.")
    
    return render_template('schedule.html', veterinarians=veterinarians, veterinarian_home_visit=veterinarian_home_visit, available_times=available_times)

@app.route('/appointments')
def view_appointments():
    if 'username' not in session:
        flash('Please log in to view appointments.')
        return redirect(url_for('login'))

    user_appointments = [appt for appt in appointments if appt['username'] == session['username']]
    return render_template('appointments.html', appointments=user_appointments)

if __name__ == '__main__':
    appointments = load_appointments()
    app.run(debug=True)
