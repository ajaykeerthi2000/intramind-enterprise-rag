from jose import jwt
import time
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

payload = {
    "sub": "ajay@company.com",
    "name": "Ajay Keerthi",
    "groups": ["RAG-App-Users"],
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600,  # 1 hour
}

token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

print(token)
