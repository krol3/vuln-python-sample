# VULNERABILITY DEMONSTRATION

a Python application that demonstrates a common code vulnerability along with a Dockerfile. I'll use SQL injection as the example vulnerability, which is educational and helps developers understand security risks.

This Flask application intentionally contains SQL injection vulnerabilities for educational purposes:

## Vulnerabilities demonstrated

1. SQL Injection in Login: Direct string concatenation in SQL queries allows attackers to bypass authentication
2. SQL Injection in Search: Unescaped user input in search functionality allows data extraction

Key vulnerable code patterns:

f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
Direct string interpolation without parameterized queries

SQL Injection examples provided:

Authentication bypass: admin' --
Always-true conditions: ' OR '1'='1' --
Data extraction: ' UNION SELECT username,password,email,role FROM users --

## Run the application

```
python3 app.py
```


## setting local environment

```
python3 -m venv myenv
source myenv/bin/activate
```

Create the first time the requirements

```
pip install flask
pip freeze > requirements.txt
```