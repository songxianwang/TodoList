# -*- coding: utf-8 -*-
# @Author  : sxw
# @Time    : 2025/11/25 11:33
# @Desc    : 路由-curd
from typing import List
from fastapi import HTTPException
from src.config.database import fake_db
from src.models.Todo import *
from fastapi import APIRouter

todo_app = APIRouter()

# 1. 获取所有待办事项 (Read All)
@todo_app.get("/", response_model=List[Todo])
async def get_todos(skip: int = 0, limit: int = 10):
    """
    获取待办事项列表，支持分页 (skip, limit)
    """
    return fake_db[skip: skip + limit]


# 2. 获取单个待办事项 (Read One)
@todo_app.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """
    根据 ID 获取具体的待办事项
    """
    for todo in fake_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="未找到该待办事项 (Todo not found)")


# 3. 创建待办事项 (Create)
@todo_app.post("/", response_model=Todo, status_code=201)
async def create_todo(todo_in: TodoCreate):
    """
    创建一个新的待办事项
    """
    # 简单的 ID 生成逻辑：取最后一个 ID + 1，如果是空的则设为 1
    new_id = 1
    if fake_db:
        new_id = fake_db[-1].id + 1

    # 将输入数据转换为数据库模型
    new_todo = Todo(id=new_id, **todo_in.model_dump())
    fake_db.append(new_todo)
    return new_todo


# 4. 更新待办事项 (Update)
@todo_app.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_in: TodoCreate):
    """
    更新已存在的待办事项
    """
    for index, todo in enumerate(fake_db):
        if todo.id == todo_id:
            # 更新逻辑：保留 ID，更新其他字段
            updated_todo = todo.model_copy(update=todo_in.model_dump())
            fake_db[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="未找到该待办事项")


# 5. 删除待办事项 (Delete)
@todo_app.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    """
    删除指定的待办事项
    """
    for index, todo in enumerate(fake_db):
        if todo.id == todo_id:
            del fake_db[index]
            return {"message": "删除成功", "deleted_id": todo_id}
    raise HTTPException(status_code=404, detail="未找到该待办事项")