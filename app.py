import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is required for Supabase/PostgreSQL")


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def get_db_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def user_to_dict(user):
    created_at = user["created_at"]
    if hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "created_at": created_at,
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

    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return jsonify({"error": "Username already exists"}), 400

        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"error": "Email already exists"}), 400

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        cur.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
            RETURNING id, username, email, created_at
            """,
            (username, email, hashed_password),
        )
        user = cur.fetchone()
        conn.commit()

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user": user_to_dict(user),
                }
            ),
            201,
        )
    except Exception:
        conn.rollback()
        return jsonify({"error": "Registration failed"}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = (data.get("username") or "").strip()
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        cur.execute(
            """
            SELECT id, username, email, password, created_at
            FROM users
            WHERE username = %s OR email = %s
            LIMIT 1
            """,
            (username, username),
        )
        user = cur.fetchone()

        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

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
    finally:
        cur.close()
        conn.close()


@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    cur = get_db_cursor(conn)

    try:
        cur.execute(
            """
            SELECT id, username, email, created_at
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        )
        user = cur.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user_to_dict(user))
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=False, port=port)
