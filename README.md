# Login Form with Flask Backend

A simple login and registration system using Python Flask with SQLite database.

## Features
- User registration with username, email, and password
- User login with username or email and password
- Flask backend with SQLAlchemy ORM
- SQLite database for user storage
- Password hashing using Werkzeug
- Modern, responsive UI
- Dashboard with profile picture and stats

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000/
```

## Files
- `app.py` - Flask application with API endpoints
- `requirements.txt` - Python dependencies
- `login.html` - Login page
- `register.html` - Registration page
- `dashboard.html` - Dashboard page
- `styles.css` - Styling for all pages
- `login.js` - Login form JavaScript
- `register.js` - Registration form JavaScript
- `dashboard.js` - Dashboard JavaScript
- `users.db` - SQLite database (created automatically)

## API Endpoints

- `POST /api/register` - Register a new user
  - Body: `{ "username": "...", "email": "...", "password": "..." }`
  
- `POST /api/login` - Login a user
  - Body: `{ "username": "...", "password": "..." }`
  - Note: username can be either username or email

- `GET /api/user/<id>` - Get user information

## Database Schema

The `users` table has the following columns:
- `id` - Primary key (auto-increment)
- `username` - Unique username
- `email` - Unique email address
- `password` - Hashed password
- `created_at` - Timestamp of account creation
