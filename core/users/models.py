from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from passlib.context import CryptContext

from core.database import Base


""" hashing password """
pwd_context = CryptContext(schemes="scrypt",deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)
    created_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    updated_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),server_onupdate=func.now())

    """ relationships """
    profile = relationship("ProfileModel",back_populates="user")
    token = relationship("TokenModel",back_populates="user")

    def hash_password(self, plain_text: str):
        return pwd_context.hash(plain_text)
    
    def verify_password(self, plain_text: str):
        return pwd_context.verify(plain_text, self.password)
    
    def set_password(self, plain_text: str) -> None:
        self.password = self.hash_password(plain_text)


class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
    first_name: Mapped[str] = mapped_column(String(75),nullable=True)
    last_name: Mapped[str] = mapped_column(String(75),nullable=True)
    bio: Mapped[str] = mapped_column(Text,nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    updated_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),server_onupdate=func.now())

    """ relationships """
    user = relationship("UserModel",back_populates="profile",uselist=False)


class TokenModel(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())

    user = relationship("UserModel",back_populates="token",uselist=False)