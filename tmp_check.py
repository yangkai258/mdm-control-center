import bcrypt
h = b'$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy'
print('Hash matches password:', bcrypt.checkpw(b'password', h))
