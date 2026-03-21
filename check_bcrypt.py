import bcrypt
hash_from_db = '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy'
print("Hash length:", len(hash_from_db))
print("Check password:", bcrypt.checkpw(b'password', hash_from_db.encode()))
