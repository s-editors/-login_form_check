import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from supabase import Client, create_client
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Set SUPABASE_URL and SUPABASE_SERVICE_KEY in your environment or .env file"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def user_to_dict(user):
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"],
    }


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
@app.route("/dashboard.html")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    existing_username = (
        supabase.table("users").select("id").eq("username", username).execute()
    )
    if existing_username.data:
        return jsonify({"error": "Username already exists"}), 400

    existing_email = supabase.table("users").select("id").eq("email", email).execute()
    if existing_email.data:
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    try:
        result = (
            supabase.table("users")
            .insert(
                {
                    "username": username,
                    "email": email,
                    "password": hashed_password,
                }
            )
            .execute()
        )

        if not result.data:
            return jsonify({"error": "Registration failed"}), 500

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user": user_to_dict(result.data[0]),
                }
            ),
            201,
        )
    except Exception:
        return jsonify({"error": "Registration failed"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = (data.get("username") or "").strip()
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    result = (
        supabase.table("users")
        .select("id, username, email, password, created_at")
        .or_(f"username.eq.{username},email.eq.{username}")
        .execute()
    )

    if not result.data:
        return jsonify({"error": "Invalid username or password"}), 401

    user = result.data[0]

    if check_password_hash(user["password"], password):
        return (
            jsonify(
                {
                    "message": "Login successful",
                    "user": user_to_dict(user),
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    result = (
        supabase.table("users")
        .select("id, username, email, created_at")
        .eq("id", user_id)
        .execute()
    )

    if not result.data:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_to_dict(result.data[0]))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
