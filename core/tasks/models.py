from sqlalchemy import Column,Integer,String,Text,DateTime,Boolean,func,ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    title = Column(String(100),nullable=False)
    description = Column(Text,nullable=True)
    is_completed = Column(Boolean,default=False,nullable=False)
    created_date = Column(DateTime,server_default=func.now(),nullable=False)
    updated_date = Column(DateTime,server_default=func.now(),server_onupdate=func.now(),nullable=False)

    user = relationship("UserModel",back_populates="task")