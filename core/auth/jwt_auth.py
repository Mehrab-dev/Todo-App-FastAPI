from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
import time

from core.settings import setting
from core.database import get_db
from users.models import UserModel

security = HTTPBearer()


def get_authenticated_user(
    credentials:HTTPAuthorizationCredentials = Depends(security),
    db:Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms="HS256")
        user_id = decoded.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, user_id not in  the payload")
        if not decoded.get("type") == "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, token type not valid")
        
        user = db.query(UserModel).filter_by(id=user_id).one()
        return user
    
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, decode field")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, token expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Authentication field, error : {e}")


def generate_access_token(
    user_id:int,
    expired_in:int = 180
):
    now = time.time()
    payload = {
        "type":"access",
        "user_id":user_id,
        "iat":now,
        "exp":now + expired_in
    }

    return jwt.encode(payload, setting.JWT_SECRET_KEY, algorithm="HS256")


def generate_refresh_token(
    user_id:int,
    expired_in:int = 3600*24
):
    now = time.time()
    payload = {
        "type":"refresh",
        "user_id":user_id,
        "iat":now,
        "exp":now + expired_in
    }

    return jwt.encode(payload, setting.JWT_SECRET_KEY, algorithm="HS256")


def decode_refresh_token(
    token:str
):
    try:
        decoded = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms="HS256")
        user_id = decoded.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, user_id not in the payload")
        if not decoded.get("type") == "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, tpken type not valid")
        return user_id
    
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, decode field")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication field, token expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Authentication field, errors : {e}")
