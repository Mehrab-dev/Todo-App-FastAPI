from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .schemas import UserLoginSchema, UserSignUpSchema
from .models import UserModel, ProfileModel
from core.database import get_db

router = APIRouter()


@router.post("/signup")
async def user_signup(
    request: UserSignUpSchema,
    db:Session = Depends(get_db)
):
    exists_user = db.query(UserModel).filter_by(email=request.email).first()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user already exists")
    else:
        user = UserModel(email=request.email)
        user.set_password(request.password)
        db.add(user)
        db.commit()

        """ creating profile for user """
        profile = ProfileModel(user_id=user.id)
        db.add(profile)
        db.commit()

        return JSONResponse(status_code=status.HTTP_201_CREATED,content={"detail":"user added successfully"})
    

@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    db:Session = Depends(get_db)
):
    user = db.query(UserModel).filter_by(email=request.email).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,detail="user not found")
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,content={"detail":"user logged successfully"})
    