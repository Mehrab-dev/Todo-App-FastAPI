from sqlalchemy import Column,String,Integer,Text,DateTime,Boolean,func,ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from core.database import Base

pwd_context = CryptContext(schemes=["scrypt"],deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    is_active = Column(Boolean,default=True,nullable=False)
    created_date = Column(DateTime,server_default=func.now(),nullable=False)
    updated_date = Column(DateTime,server_default=func.now(),server_onupdate=func.now(),nullable=False)

    profile = relationship("ProfileModel",back_populates="user")

    def hash_password(self,plain_text: str):
        return pwd_context.hash(plain_text)
    
    def verify_password(self,plain_text: str):
        return pwd_context.verify(plain_text,self.password)
    
    def set_password(self,plain_text: str) -> None:
        self.password = self.hash_password(plain_text)



class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    first_name = Column(String(50),nullable=True)
    last_name = Column(String(50),nullable=True)
    bio = Column(Text,nullable=True)

    user = relationship("UserModel",back_populates="profile",uselist=False)