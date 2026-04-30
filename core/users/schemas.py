from pydantic import BaseModel,Field,EmailStr,field_validator


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