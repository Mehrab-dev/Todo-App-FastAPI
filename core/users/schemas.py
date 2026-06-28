from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional


class UserSignUpSchema(BaseModel):
    email: EmailStr = Field(...,description="email of the user for signup")
    password: str = Field(...,description="password of the user for signup")
    confirm_password: str = Field(...,description="confirm password of the user")

    @field_validator("confirm_password")
    def check_password_match(cls, confirm_password, validation):
        if not (confirm_password == validation.data.get("password")):
            raise ValueError("password does not match")


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...,description="email of the user for login")
    password: str = Field(...,description="password of the user for login")


class RefreshTokenSchema(BaseModel):
    token: str = Field(...,description="refresh token for geting access token")


class ResetPasswordSchema(BaseModel):
    email: EmailStr = Field(...,description="email of the user for reset password")
    new_password: str = Field(...,description="new password of the user for reset password")
    confirm_new_password: str = Field(...,description="confirm new password of the user for reset password")

    @field_validator("confirm_new_password")
    def check_password_match(cls, confirm_new_password, validation):
        if not (confirm_new_password == validation.data.get("new_password")):
            raise ValueError("password does not match")


class UpdatePasswordSchema(BaseModel):
    new_password: str = Field(...,description="new password of the user for update password")
    confirm_new_password: str = Field(...,description="confirm new password of the user for update password")

    @field_validator("confirm_new_password")
    def check_password_match(cls, confirm_new_password, validation):
        if not (confirm_new_password == validation.data.get("new_password")):
            raise ValueError("password does not match")
        

class UpdateEmailSchema(BaseModel):
    new_email: str = Field(...,description="email of the user for update email")


class UpdateProfileSchema(BaseModel):
    first_name: Optional[str] = Field(None, max_length=75, description="first name of the user")
    last_name: Optional[str] = Field(None, max_length=75, description="last name of the user")
    bio: Optional[str] = Field(None, max_length=600, description="bio of the user")