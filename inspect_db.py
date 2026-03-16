import sqlite3

conn = sqlite3.connect(r'C:\Users\YKing\.openclaw\workspace\mbti_test.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in c.fetchall()]
print("=== Tables ===")
for t in tables:
    print(f"\n--- {t} ---")
    c.execute(f"PRAGMA table_info({t})")
    for col in c.fetchall():
        print(f"  {col[1]} ({col[2]})")
    c.execute(f"SELECT COUNT(*) FROM [{t}]")
    print(f"  Rows: {c.fetchone()[0]}")

conn.close()
