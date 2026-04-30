from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime


class TaskCreateSchema(BaseModel):
    title: str = Field(...,max_length=100,description="Title of the task")
    description: Optional[str] = Field(None,max_length=600,description="Description of the task")
    is_completed: bool = Field(...,description="State of the task")


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None,max_length=100,description="Title of the task for update task")
    description: Optional[str] = Field(None,max_length=600,description="Description of the task for update task")
    is_completed: Optional[bool] = Field(None,description="State of the task for update task")


class TaskResponseSchema(BaseModel):
    id: int = Field(description="Unique identifier of the task")
    title: str = Field(description="Title of the task for response")
    description: str = Field(description="Description of the task for response")
    is_completed: bool = Field(description="State of the task for response")
    created_date: datetime = Field(description="Creation date and time of the task for response")
    updated_date: datetime = Field(description="Updating date and time of the task for response")
    