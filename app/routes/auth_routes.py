from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
import requests
from app.models import RegisteredUser, LoginAttempt
from app import db
from app.utils import hash_password, verify_password
from werkzeug.utils import secure_filename
import os

auth_bp = Blueprint("auth", __name__)

# Define a folder to store uploaded profile pictures
UPLOAD_FOLDER = 'profile_pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Make sure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Login Route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user exists
        user = RegisteredUser.query.filter_by(email=email).first()
        if user and verify_password(password, user.password):
            login_attempt = LoginAttempt(email=email, status="Success")
            db.session.add(login_attempt)
            db.session.commit()
            flash("Login successful!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            login_attempt = LoginAttempt(email=email, status="Failed")
            db.session.add(login_attempt)
            db.session.commit()
            flash("Invalid email or password!", "error")
    return render_template("login.html")

# Register Route
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone_number = request.form.get("phone_number")
        address = request.form.get("address")
        date_of_birth = request.form.get("date_of_birth")
        profile_picture = request.files.get("profile_picture")

        if not first_name or not last_name or not email or not password:
            flash("Please fill in all the required fields.", "error")
            return redirect(url_for("auth.register"))

        if RegisteredUser.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
        else:
            filename = None
            if profile_picture and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(UPLOAD_FOLDER, filename))
            
            new_user = RegisteredUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hash_password(password),
                phone_number=phone_number,
                address=address,
                date_of_birth=date_of_birth,
                profile_picture=filename
            )
            db.session.add(new_user)
            db.session.commit()

            login_attempt = LoginAttempt(email=email, status="Success")
            db.session.add(login_attempt)
            db.session.commit()

            flash("Registration successful!", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/dashboard")
def dashboard():
    user = RegisteredUser.query.first()
    user_name = user.name if user else "Guest"
    return render_template("home.html")

@auth_bp.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)

@auth_bp.route('/orders')
def orders():
    return render_template('orders.html')

ALPHA_VANTAGE_API_KEY = "TZZ4861X7WGGQJYR"

def get_stock_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (5min)" in data:
        latest_time = sorted(data["Time Series (5min)"].keys())[-1]
        stock_info = data["Time Series (5min)"][latest_time]
        return {
            "name": symbol,
            "symbol": symbol,
            "price": round(float(stock_info["1. open"]), 2),
            "change": round(float(stock_info["4. close"]) - float(stock_info["1. open"]), 2),
            "volume": stock_info["5. volume"]
        }
    return None

@auth_bp.route('/stocks')
def stocks_view():
    sample_stocks = [
        {"name": "Apple", "symbol": "AAPL", "price": 185.32, "change": 1.24, "volume": "78M"},
        {"name": "Microsoft", "symbol": "MSFT", "price": 342.15, "change": -0.85, "volume": "54M"},
        {"name": "Tesla", "symbol": "TSLA", "price": 217.56, "change": 2.14, "volume": "31M"},
        {"name": "Amazon", "symbol": "AMZN", "price": 145.20, "change": -1.45, "volume": "40M"},
    ]
    return render_template('stocks.html', stocks=sample_stocks)
