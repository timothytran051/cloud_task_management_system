import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()
key = os.getenv("SECRET_KEY")

def hash_password(plain_password:str ) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

#test hashing
# hashed_pw = hash_password("password123")
# print (hashed_pw)

#test verify
# stored_hash = hash_password("password123")
# print(verify_password("password123", stored_hash))
# print(verify_password("wrongpass", stored_hash))

def generate_token(payload, key):
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    payload.update({
        "sub": str(payload["sub"]),
        "exp": expiration_time
    })
    try:
        token = jwt.encode(payload, key, algorithm="HS256")
        # print(f"token: {token}")
        return token
    except Exception as e:
        print(f"⚠️ JWT Encoding Error: {e}")
        return None
    # expiration_time = datetime.utcnow() + timedelta(minutes=30)
    # payload.update({       
    #     "exp": expiration_time})
    # token = jwt.encode(payload, key, algorithm = "HS256")

def verify_token(token, key):
    try:
        # print(f"first pass: {token}")
        # print(f"key: {key}")
        verify = jwt.decode(token, key, algorithms=["HS256"])
        # print(f"after pass: {verify}")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired Token")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid Signature")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return verify
