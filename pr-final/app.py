from flask import Flask, render_template, session, redirect
from functools import wraps
from datetime import datetime
import pymongo

app = Flask(__name__)
app.secret_key = "Ayyan-Junaid"

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

# Decorators
def login_required(f):  
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    
    return wrap

# Routes
from user import routes

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/signup/')
def signup_page():
    return render_template('signup.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    # try:
    name = session['user']['name']
    date_time = datetime.now()
    today_date = date_time.strftime("%d-%m-%Y")
    if db.employee_time.find_one({ "name": name, "status": "check-in", "date": today_date },{"time":1,"_id":0,}):
        checkin_time1 = db.employee_time.find_one({ "name": name, "status": "check-in", "date": today_date },{"time":1,"_id":0,})
        checkin_time = checkin_time1.get("time")
    else:
        checkin_time = "00:00:00"
    if db.employee_time.find_one({ "name": name, "status": "check-out", "date": today_date },{"time":1,"_id":0,}):     
        checkout_time1 = db.employee_time.find_one({ "name": name, "status": "check-out", "date": today_date },{"time":1,"_id":0,})
        checkout_time = checkout_time1.get("time")
    else:
        checkout_time = "00:00:00"

    return render_template('dashboard.html', checkin_time = checkin_time, checkout_time = checkout_time, today_date = today_date)
    
    # except:
    #     checkin_time = "00:00:00"
    #     checkout_time = "00:00:00"
    #     date_time = datetime.now()
    #     today_date = date_time.strftime("%d-%m-%Y")
    #     return render_template('dashboard.html', checkin_time = checkin_time, checkout_time = checkout_time, today_date = today_date)


@app.route('/admin/dashboard/')
@login_required
def admin_dashboard():
    return render_template('admin-dashboard.html')



