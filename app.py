import os, secrets, logging
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure DB path is absolute (prevents file path issues)
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "users.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), unique=True, nullable=True)

with app.app_context():
    db.create_all()

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"success": False, "message": "Missing email or password."}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"Signed up: {email}")
        return jsonify({"success": True, "message": "Signup successful! Please login."}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "Email already registered."}), 409
    except Exception as e:
        app.logger.exception("Signup error")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"success": False, "message": "Missing email or password."}), 400

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            if not user.token:
                user.token = secrets.token_hex(16)
                db.session.commit()
            app.logger.info(f"Login success: {email}")
            return jsonify({"success": True, "message": "Login successful!", "token": user.token}), 200
        else:
            app.logger.info(f"Login failed for {email}")
            return jsonify({"success": False, "message": "Invalid email or password."}), 401
    except Exception as e:
        app.logger.exception("Login error")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/validate", methods=["POST"])
def validate():
    try:
        data = request.get_json(force=True)
        token = data.get("token")
        if not token:
            return jsonify({"success": False, "message": "No token provided."}), 400
        user = User.query.filter_by(token=token).first()
        if user:
            return jsonify({"success": True, "email": user.email}), 200
        else:
            return jsonify({"success": False, "message": "Invalid token."}), 401
    except Exception as e:
        app.logger.exception("Validate error")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)


