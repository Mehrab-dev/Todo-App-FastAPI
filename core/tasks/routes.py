from fastapi import APIRouter,status,HTTPException,Depends,Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from tasks.schemas import (TaskCreateSchema,TaskUpdateSchema,TaskResponseSchema)
from core.database import get_db
from tasks.models import TaskModel
from users.models import UserModel
from auth.jwt_auth import get_authenticated_user


router = APIRouter(tags=["tasks"])


@router.get("/tasks",response_model=List[TaskResponseSchema])
async def tasks_list(
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    tasks = db.query(TaskModel).filter_by(user_id=user.id).all()
    return tasks


@router.get("/tasks/{task_id}",response_model=TaskResponseSchema)
async def task_detail(
    task_id: int = Path(...,gt=0),
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    task = db.query(TaskModel).filter_by(id=task_id,user_id=user.id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found.")
    
    return task


@router.post("/tasks/create")
async def task_create(
    request:TaskCreateSchema,
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    data = request.model_dump()
    data.update({"user_id":user.id})
    task = TaskModel(**data)
    db.add(task)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED,content={"detail":"Task added successfully."})


@router.put("/tasks/update/{task_id}")
async def task_update(
    request: TaskUpdateSchema,
    task_id: int = Path(...,gt=0),
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    task = db.query(TaskModel).filter_by(id=task_id,user_id=user.id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_200_OK,detail="Task not found.")
    if task:
        if request.title is not None:
            task.title = request.title
        if request.description is not None:
            task.description = request.description
        if request.is_completed is not None:
            task.is_completed = request.is_completed
    db.commit()
    db.refresh(task)

    return JSONResponse(status_code=status.HTTP_200_OK,content={"detail":"Task updated successfully."})


@router.delete("/tasks/delete/{task_id}")
async def task_delete(
    task_id: int = Path(...,gt=0),
    db:Session = Depends(get_db),
    user:UserModel = Depends(get_authenticated_user)
):
    task = db.query(TaskModel).filter_by(id=task_id,user_id=user.id).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found.")
    db.delete(task)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,content={"detail":"Task deleted successfully."})