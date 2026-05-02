from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import  Session
import secrets

from users.schemas import UserSignupSchema,UserLoginSchema
from core.database import get_db
from users.models import UserModel,ProfileModel,TokenModel
from auth.jwt_auth import generate_access_token,generate_refresh_token


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