from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import  Session
import secrets

from users.schemas import (UserSignupSchema,UserLoginSchema,RefreshTokenSchema,UpdateEmailSchema,
                           UpdatePasswordSchema,UpdateProfileSchema)
from core.database import get_db
from users.models import UserModel,ProfileModel,TokenModel
from auth.jwt_auth import generate_access_token,generate_refresh_token,decode_refresh_token,get_authenticated_user


router = APIRouter(tags=["users"])


@router.post("/signup")
async def signup(
    request:UserSignupSchema,
    db:Session = Depends(get_db)
):
    exists_user = db.query(UserModel).filter_by(email=request.email).first()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists.")
    user = UserModel(email=request.email)
    user.set_password(request.password)
    db.add(user)
    db.commit()

    """ Create Profile for user """
    profile = ProfileModel(user_id=user.id)
    db.add(profile)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED,content={"detail":"User added successfully."})


def generate_token(lenght= 32):
    return secrets.token_hex(lenght)


@router.post("/login")
async def login(
    request:UserLoginSchema,
    db:Session = Depends(get_db)
):
    user = db.query(UserModel).filter_by(email=request.email).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Inccorect email or password.")
    if not user.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Inccorect email or password.")
    
    # """ Delete the user ids previous token """
    # exists_token = db.query(TokenModel).filter_by(user_id=user.id).first()
    # if exists_token:
    #     db.delete(exists_token)
    #     db.commit()
    
    # """ Create a new token for the user """
    # token = TokenModel(user_id=user.id,token=generate_token())
    # db.add(token)
    # db.commit()
    # db.refresh(token)

    """ Create access token and refresh token for user """
    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)

    return JSONResponse(status_code=status.HTTP_200_OK,content={"detail":"Logged in successfully.",
                                                                "access-token":access_token,
                                                                "refresh-token":refresh_token})


""" get access token with refresh token """
@router.post("/get/access-token")
async def get_access_token(
    request: RefreshTokenSchema
):
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id)

    return JSONResponse({"access-token":access_token})


""" endpoint for updating email """
@router.put("/user/update/email")
async def update_email(
    request: UpdateEmailSchema,
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    user.email = request.email
    db.commit()
    db.refresh(user)

    return JSONResponse(status_code=status.HTTP_200_OK,content={"detail":"Email updated successfully."})


""" endpoint for updaing password """
@router.put("/user/update/password")
async def update_password(
    request: UpdatePasswordSchema,
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    user.set_password(request.new_password)
    db.commit()
    db.refresh(user)

    return JSONResponse(status_code=status.HTTP_200_OK,content={"detail":"Password updated successfully."})


""" endpoint for completing profile """
@router.put("/user/profile")
async def update_profile(
    request: UpdateProfileSchema,
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    profile = db.query(ProfileModel).filter_by(user_id=user.id).one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Profile not found of the user")
    
    if request.first_name is not None:
        profile.first_name = request.first_name
    if request.last_name is not None:
        profile.last_name = request.last_name
    if request.bio is not None:
        profile.bio = request.bio

    db.commit()
    db.refresh(profile)
    return JSONResponse(status_code=status.HTTP_200_OK,content={"detail":"Profile updated successfully."})