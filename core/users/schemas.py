from pydantic import BaseModel, Field, EmailStr, field_validator


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
