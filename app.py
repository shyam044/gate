from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import os, secrets

app = Flask(__name__, static_folder="static")
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), unique=True, nullable=True)

with app.app_context():
    db.create_all()

# ---------- API ----------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password."})

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": True, "message": "Signup successful! Please login."})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "Email already registered."})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        # Generate new token if not already
        if not user.token:
            user.token = secrets.token_hex(16)
            db.session.commit()
        return jsonify({"success": True, "message": "Login successful!", "token": user.token})
    else:
        return jsonify({"success": False, "message": "Invalid email or password."})

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    token = data.get("token")
    user = User.query.filter_by(token=token).first()
    if user:
        return jsonify({"success": True, "email": user.email})
    else:
        return jsonify({"success": False})

# ---------- Serve Frontend ----------

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)


