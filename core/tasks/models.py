from sqlalchemy import Integer, String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255),nullable=False)
    description: Mapped[str] = mapped_column(Text,nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean,default=False)
    created_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    updated_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),server_onupdate=func.now())

    user = relationship("UserModel", back_populates="tasks")
