import bcrypt

def hash_password(plain_password:str ) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hash_password.encode('utf-8'))

hashed_pw = hash_password("password123")
print (hashed_pw)
verify = verify_password("password123","$2b$12$EI16n/wsP0QDvUnexBHl3On692MFy2ErU5b0H8iaXf3bhHYGY9ewm")