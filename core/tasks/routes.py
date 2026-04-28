from fastapi import APIRouter,status,HTTPException,Depends,Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from tasks.schemas import (TaskCreateSchema,TaskUpdateSchema,TaskResponseSchema)
from core.database import get_db
from tasks.models import TaskModel


router = APIRouter()


@router.get("/tasks",response_model=TaskResponseSchema)
async def tasks_list(
    db:Session = Depends(get_db)
):
    tasks = db.query(TaskModel)
    return tasks


@router.get("/tasks/{task_id}",response_model=TaskResponseSchema)
async def task_detail(
    task_id: int = Path(...,gt=0),
    db:Session = Depends(get_db)
):
    task = db.query(TaskModel).filter_by(id=task_id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found.")
    
    return task


@router.post("/tasks/create")
async def task_create(
    request:TaskCreateSchema,
    db:Session = Depends(get_db),
):
    task = TaskModel(**request.model_dump())
    db.add(task)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED,content={"detail":"Task added successfully."})


@router.put("/tasks/update/{task_id}")
async def task_update(
    request: TaskUpdateSchema,
    task_id: int = Path(...,gt=0),
    db:Session = Depends(get_db)
):
    task = db.query(TaskModel).filter_by(id=task_id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_200_OK,detail="Task not found.")
    