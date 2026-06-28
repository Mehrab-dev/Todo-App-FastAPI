from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import secrets

from .schemas import (UserLoginSchema, UserSignUpSchema, RefreshTokenSchema, ResetPasswordSchema, UpdatePasswordSchema,
                      UpdateEmailSchema, UpdateProfileSchema)
from .models import UserModel, ProfileModel, TokenModel
from core.database import get_db
from auth.jwt_auth import generate_access_token, generate_refresh_token, decode_refresh_token, get_authenticated_user

router = APIRouter(tags=["users"])

""" generate token """
def generate_token(length=32):
    return secrets.token_hex(length)


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

        """ creating token for user """
        token = TokenModel(user_id=user.id,token=generate_token())
        db.add(token)
        db.commit()

        return JSONResponse(status_code=status.HTTP_201_CREATED,content={"detail":"user added successfully"})
    

@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    db:Session = Depends(get_db)
):
    user = db.query(UserModel).filter_by(email=request.email).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="inccorect email or password")
    if not user.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="inccorect email or password")
    
    """ create access token and refresh token """
    access_token = generate_access_token(user_id=user.id)
    refresh_token = generate_refresh_token(user_id=user.id)

    return JSONResponse(status_code=status.HTTP_200_OK,content={"detail":"user logged successfully","access-token":access_token,"refresh-token":refresh_token})


@router.post("/get-access-token")
async def get_access_token(
    request:RefreshTokenSchema
):
    user_id = decode_refresh_token(request.token)

    """ create access token """
    access_token = generate_access_token(user_id=user_id)
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"access-token":access_token})


@router.post("/password/reset")
async def reset_password(
    request:ResetPasswordSchema,
    db:Session = Depends(get_db),
):
    user = db.query(UserModel).filter_by(email=request.email).one_or_none()
    if user:
        user.password = user.hash_password(request.new_password)
        db.commit()
        db.refresh(user)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail":"reset password successfully"})
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="there is no user with this email")
    

@router.put("/password/update")
async def password_update(
    request:UpdatePasswordSchema,
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    user.password = user.hash_password(request.new_password)
    db.commit()
    db.refresh(user)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail":"updated password successfully"})


@router.put("/email/update")
async def email_update(
    request:UpdateEmailSchema,
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    user.email = request.new_email
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail":"email updated successfully"})


@router.put("/profile/update")
async def profile_update(
    request:UpdateProfileSchema,
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    profile = db.query(ProfileModel).filter_by(user_id=user.id).one()
    if request.first_name is not None:
        profile.first_name = request.first_name
    if request.last_name is not None:
        profile.last_name = request.last_name
    if request.bio is not None:
        profile.bio = request.bio
    
    db.commit()
    db.refresh(profile)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail":"profile updated successfully"})