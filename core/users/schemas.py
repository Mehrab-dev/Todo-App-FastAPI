from pydantic import BaseModel,Field,EmailStr,field_validator
from typing import Optional


class UserSignupSchema(BaseModel):
    email: EmailStr = Field(...,description="Email of the user for signup")
    password: str = Field(...,description="Password of the user")
    confirm_password: str = Field(...,description="Confirm password of the user")

    @field_validator("confirm_password")
    def check_password_match(cls,confirm_password,validation):
        if not confirm_password == validation.data.get("password"):
            raise ValueError("Password does not match")



class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...,description="Email of the user for signin")
    password: str = Field(...,description="Password of the user for signin")



class RefreshTokenSchema(BaseModel):
    token: str = Field(...,description="Refresh token to create access token")


""" Schema for Updating Email """
class UpdateEmailSchema(BaseModel):
    email: EmailStr = Field(...,description="Email of the user for update email")


""" Schema for updating password """
class UpdatePasswordSchema(BaseModel):
    new_password: str = Field(...,description="New password for updating password")
    confirm_new_password: str = Field(...,description="Confirm new password for updating password")

    @field_validator("confirm_new_password")
    def check_match_password(cls,confirm_new_password,validation):
        if not confirm_new_password == validation.data.get("new_password"):
            raise ValueError("password does not match")
        

""" Schema for Completing or Updating profile """
class UpdateProfileSchema(BaseModel):
    first_name: Optional[str] = Field(None,max_length=50,description="First name for completing or updating profile of the user")
    last_name: Optional[str] = Field(None,max_length=50,description="Last name for completing or updating profile of the user")
    bio: Optional[str] = Field(None,max_length=500,description="Bio for completing or updating profile of the user")