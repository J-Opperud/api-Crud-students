python -c  → test Python code directly
curl       → test  API endpoints



## Auth commands

- Create a token for user ID 1

python -c "from app.utils.security import create_access_token; print(create_access_token({'sub': '1'}))"

- Create a token for user ID 2

python -c "from app.utils.security import create_access_token; print(create_access_token({'sub': '2'}))"

- Test password hashing

python -c "from app.utils.security import hash_password; print(hash_password('TestPass123'))"

- Test password verification

python -c "from app.utils.security import verify_password; print(verify_password('TestPass123', 'PASTE_HASH_HERE'))"

- Test that security imports correctly

python -c "from app.utils.security import get_current_user; print('security import OK')"

## Database checks

- See all users

python -c "import sqlite3; c=sqlite3.connect('students.db').cursor(); print(c.execute('SELECT id, users_name, email FROM users').fetchall())"

- See database tables

python -c "import sqlite3; c=sqlite3.connect('students.db').cursor(); print(c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall())"

- See students

python -c "import sqlite3; c=sqlite3.connect('students.db').cursor(); print(c.execute('SELECT * FROM students').fetchall())"




curl http://127.0.0.1:8000/students

curl -X POST "http://127.0.0.1:8000/students" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"John Smith","email":"john@example.com","grade_level":10,"gpa":3.5,"is_enrolled":true}'


Test /users/me with the token


curl "http://127.0.0.1:8000/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X PATCH "http://127.0.0.1:8000/students/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"John Updated","grade_level":11,"gpa":3.9}'




