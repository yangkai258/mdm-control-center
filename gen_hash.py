import bcrypt
password = b'admin123'
h = bcrypt.hashpw(password, bcrypt.gensalt())
print("Hash:", h.decode())
print("Check:", bcrypt.checkpw(password, h))
