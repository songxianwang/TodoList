from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="简易待办事项 API",
    description="使用 FastAPI 构建的 Todo List 演示项目",
    version="1.0.0"
)


# --- 数据模型 (Pydantic Models) ---

# 基础模型：包含共享字段
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False


# 创建时使用的模型：不需要 ID (由后端生成)
class TodoCreate(TodoBase):
    pass


# 响应和数据库存储使用的模型：包含 ID
class Todo(TodoBase):
    id: int


# --- 模拟数据库 ---
fake_db: List[Todo] = []


# --- 路由 (Endpoints) ---

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "欢迎使用 Todo API! 请访问 /docs 查看文档。"}


# 1. 获取所有待办事项 (Read All)
@app.get("/todos", response_model=List[Todo], tags=["Todos"])
async def get_todos(skip: int = 0, limit: int = 10):
    """
    获取待办事项列表，支持分页 (skip, limit)
    """
    return fake_db[skip: skip + limit]


# 2. 获取单个待办事项 (Read One)
@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def get_todo(todo_id: int):
    """
    根据 ID 获取具体的待办事项
    """
    for todo in fake_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="未找到该待办事项 (Todo not found)")


# 3. 创建待办事项 (Create)
@app.post("/todos", response_model=Todo, status_code=201, tags=["Todos"])
async def create_todo(todo_in: TodoCreate):
    """
    创建一个新的待办事项
    """
    # 简单的 ID 生成逻辑：取最后一个 ID + 1，如果是空的则设为 1
    new_id = 1
    if fake_db:
        new_id = fake_db[-1].id + 1

    # 将输入数据转换为数据库模型
    new_todo = Todo(id=new_id, **todo_in.dict())
    fake_db.append(new_todo)
    return new_todo


# 4. 更新待办事项 (Update)
@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def update_todo(todo_id: int, todo_in: TodoCreate):
    """
    更新已存在的待办事项
    """
    for index, todo in enumerate(fake_db):
        if todo.id == todo_id:
            # 更新逻辑：保留 ID，更新其他字段
            updated_todo = todo.copy(update=todo_in.dict())
            fake_db[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="未找到该待办事项")


# 5. 删除待办事项 (Delete)
@app.delete("/todos/{todo_id}", tags=["Todos"])
async def delete_todo(todo_id: int):
    """
    删除指定的待办事项
    """
    for index, todo in enumerate(fake_db):
        if todo.id == todo_id:
            del fake_db[index]
            return {"message": "删除成功", "deleted_id": todo_id}
    raise HTTPException(status_code=404, detail="未找到该待办事项")
