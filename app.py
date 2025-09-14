#!/usr/bin/env python3
"""
EDUCATIONAL VULNERABILITY DEMONSTRATION
This code intentionally contains SQL injection vulnerabilities for educational purposes.
DO NOT use this pattern in production applications.
"""

from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
PORT=50005

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Insert sample data
    cursor.execute("DELETE FROM users")  # Clear existing data
    sample_users = [
        ('admin', 'admin123', 'admin@example.com', 'admin'),
        ('john_doe', 'password', 'john@example.com', 'user'),
        ('jane_smith', 'secret', 'jane@example.com', 'user'),
        ('bob_wilson', 'mypass', 'bob@example.com', 'user')
    ]
    
    for user in sample_users:
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            user
        )
    
    conn.commit()
    conn.close()

# VULNERABLE LOGIN FUNCTION - Contains SQL Injection
@app.route('/')
def index():
    return render_template_string('''
    <h1>Vulnerable Login Demo</h1>
    <h2>Login</h2>
    <form method="POST" action="/login">
        <p>
            Username: <input type="text" name="username" value="">
        </p>
        <p>
            Password: <input type="password" name="password" value="">
        </p>
        <p>
            <input type="submit" value="Login">
        </p>
    </form>
    
    <h2>User Search (Admin Only)</h2>
    <form method="GET" action="/search">
        <p>
            Search Username: <input type="text" name="username" value="">
        </p>
        <p>
            <input type="submit" value="Search">
        </p>
    </form>
    
    <h3>SQL Injection Examples to Try:</h3>
    <p><strong>For Login:</strong></p>
    <ul>
        <li>Username: <code>admin' --</code> Password: <code>anything</code></li>
        <li>Username: <code>' OR '1'='1' --</code> Password: <code>anything</code></li>
        <li>Username: <code>' UNION SELECT 1,2,3,4,5 --</code> Password: <code>anything</code></li>
    </ul>
    
    <p><strong>For Search:</strong></p>
    <ul>
        <li>Username: <code>' OR '1'='1</code></li>
        <li>Username: <code>' UNION SELECT username,password,email,role FROM users --</code></li>
    </ul>
    ''')

@app.route('/login', methods=['POST'])
def vulnerable_login():
    username = request.form['username']
    password = request.form['password']
    
    # VULNERABILITY: Direct string concatenation in SQL query
    # This allows SQL injection attacks
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"Executing query: {query}")  # For demonstration purposes
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return render_template_string('''
            <h1>Login Successful!</h1>
            <p><strong>User ID:</strong> {{ user_id }}</p>
            <p><strong>Username:</strong> {{ username }}</p>
            <p><strong>Email:</strong> {{ email }}</p>
            <p><strong>Role:</strong> {{ role }}</p>
            <p><a href="/">Back to Login</a></p>
            <h3>Executed Query:</h3>
            <code>{{ query }}</code>
            ''', user_id=user[0], username=user[1], email=user[3], role=user[4], query=query)
        else:
            return render_template_string('''
            <h1>Login Failed!</h1>
            <p>Invalid username or password.</p>
            <p><a href="/">Back to Login</a></p>
            <h3>Executed Query:</h3>
            <code>{{ query }}</code>
            ''', query=query)
            
    except Exception as e:
        return render_template_string('''
        <h1>Database Error!</h1>
        <p><strong>Error:</strong> {{ error }}</p>
        <p><a href="/">Back to Login</a></p>
        <h3>Executed Query:</h3>
        <code>{{ query }}</code>
        ''', error=str(e), query=query)

@app.route('/search')
def vulnerable_search():
    username = request.args.get('username', '')
    
    if not username:
        return render_template_string('''
        <h1>User Search</h1>
        <p>Please provide a username to search.</p>
        <p><a href="/">Back to Home</a></p>
        ''')
    
    # VULNERABILITY: Direct string concatenation in SQL query
    query = f"SELECT username, email, role FROM users WHERE username LIKE '%{username}%'"
    
    print(f"Executing search query: {query}")  # For demonstration purposes
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        results_html = ""
        if results:
            results_html = "<h3>Search Results:</h3><ul>"
            for row in results:
                results_html += f"<li><strong>{row[0]}</strong> - {row[1]} ({row[2]})</li>"
            results_html += "</ul>"
        else:
            results_html = "<p>No users found.</p>"
        
        return render_template_string('''
        <h1>User Search Results</h1>
        {{ results|safe }}
        <p><a href="/">Back to Home</a></p>
        <h3>Executed Query:</h3>
        <code>{{ query }}</code>
        ''', results=results_html, query=query)
        
    except Exception as e:
        return render_template_string('''
        <h1>Search Error!</h1>
        <p><strong>Error:</strong> {{ error }}</p>
        <p><a href="/">Back to Home</a></p>
        <h3>Executed Query:</h3>
        <code>{{ query }}</code>
        ''', error=str(e), query=query)

# SECURE VERSION (for comparison)
@app.route('/secure_login', methods=['POST'])
def secure_login():
    """
    This is how the login should be implemented securely using parameterized queries.
    """
    username = request.form['username']
    password = request.form['password']
    
    # SECURE: Using parameterized queries prevents SQL injection
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return f"<h1>Secure Login Successful!</h1><p>Welcome {user[1]}!</p>"
        else:
            return "<h1>Secure Login Failed!</h1><p>Invalid credentials.</p>"
            
    except Exception as e:
        return f"<h1>Error:</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    # Initialize database with sample data
    init_db()
    print("Database initialized with sample users:")
    print("- admin/admin123 (admin)")
    print("- john_doe/password (user)")
    print("- jane_smith/secret (user)")
    print("- bob_wilson/mypass (user)")
    print("\nStarting vulnerable web application...")
    print(f"Visit http://localhost:{PORT} to access the application")

    app.run(debug=True, host='0.0.0.0', port=PORT)
    