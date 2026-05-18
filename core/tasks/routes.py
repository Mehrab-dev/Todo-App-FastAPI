from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from tasks.schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from core.database import get_db
from tasks.models import TaskModel


router = APIRouter(tags=["tasks"])


@router.get("/tasks",response_model=List[TaskResponseSchema])
async def tasks_list(
    db:Session = Depends(get_db)
):
    tasks = db.query(TaskModel)
    return tasks