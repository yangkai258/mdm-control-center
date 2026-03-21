import bcrypt
# Generate a hash for 'admin123'
h = bcrypt.hashpw(b'admin123', bcrypt.gensalt(rounds=10))
print('Generated hash:', h.decode())
print('Check password:', bcrypt.checkpw(b'admin123', h))
