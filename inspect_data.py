import sqlite3, json
from datetime import datetime

conn = sqlite3.connect(r'C:\Users\YKing\.openclaw\workspace\mbti_test.db')
c = conn.cursor()

# Check sample data
print("=== Sample Users ===")
c.execute("SELECT id, username, nickname, gender, age, mbti_type, created_at FROM users")
for r in c.fetchall():
    print(r)

print("\n=== Sample Test Records ===")
c.execute("SELECT id, user_id, test_id, mbti_type, status, start_time, end_time FROM test_records")
for r in c.fetchall():
    print(r)

print("\n=== Sample Answers (first 5) ===")
c.execute("SELECT id, test_record_id, question_id, answer, score_e, score_i, score_s, score_n, score_t, score_f, score_j, score_p FROM answers LIMIT 5")
for r in c.fetchall():
    print(r)

print("\n=== Shares ===")
c.execute("SELECT * FROM shares")
for r in c.fetchall():
    print(r)

print("\n=== Posts ===")
c.execute("SELECT * FROM posts")
for r in c.fetchall():
    print(r)

conn.close()
