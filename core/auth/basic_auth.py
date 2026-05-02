from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from users.models import UserModel


security = HTTPBasic()

def get_authenticated_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db:Session = Depends(get_db)
):
    user = db.query(UserModel).filter_by(email=credentials.username).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inccorect email or password",
            headers={"WWW-Authentication":"Basic"}
        )
    
    if not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inccorect email or password",
            headers={"WWW-Authentication":"Basic"}
        )
    
    return user