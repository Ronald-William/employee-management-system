import os 
import jwt 
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES") or 30)

class JwtConfig:
    @staticmethod
    def create_access_token(data: dict)->str:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes = TOKEN_EXPIRE_MINUTES)
        payload.update({"exp" : expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(token: str)->dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    