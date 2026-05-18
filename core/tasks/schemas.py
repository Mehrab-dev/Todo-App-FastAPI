from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreateSchema(BaseModel):
    title: str = Field(...,max_length=75,description="Title of the task")
    description: Optional[str] = Field(None,max_length=500,description="Description of the task")
    is_completed: bool = Field(...,description="State of the task")


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None,max_length=75,description="Title of the user for update")
    description: Optional[str] = Field(None,max_length=500,description="Description of the user for update")
    is_completed: Optional[bool] = Field(None,description="State of the user for update")


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str = None
    is_completed: bool
    created_date: datetime
    updated_date: datetime