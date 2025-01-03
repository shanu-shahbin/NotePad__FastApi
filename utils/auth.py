from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer

# Configuration
SECRET_KEY = "shane33"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str = Security(security)) -> dict:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
