这份基于 **FastAPI** 的简易待办事项（Todo List）API 教程，旨在快速构建一个具备 **CRUD**（增删改查）功能的后端服务。

为了保持简单，我将使用\*\*内存（List列表）\*\*来模拟数据库存储数据。

-----

### 1\. 环境准备

首先，确保已经安装了 Python。然后安装 FastAPI 和 ASGI 服务器（Uvicorn）：

```bash
pip install fastapi uvicorn
```

### 2\. 完整代码实现 (`main.py`)

```python
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
    return fake_db[skip : skip + limit]

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
```

-----

### 3\. 代码解析

  * **Pydantic 模型 (`BaseModel`)**:
      * 我们定义了 `TodoBase` 来规范数据结构（自动验证数据类型）。
      * `TodoCreate` 用于接收用户输入（不含 ID）。
      * `Todo` 用于返回给用户（包含 ID）。
  * **模拟数据库 (`fake_db`)**:
      * 使用一个简单的 Python 列表 `[]` 存储数据。注意：**重启服务后数据会丢失**。
  * **装饰器 (`@app.get`, `@app.post`)**:
      * 定义了 HTTP 请求方法和路径。
  * **类型提示 (`response_model`)**:
      * FastAPI 会根据这个字段自动生成 JSON 响应文档，并过滤掉不该返回的数据。

-----

### 4\. 如何运行与测试

在终端中运行以下命令启动服务器：

```bash
uvicorn main:app --reload
```

  * `main`: 指的是文件名 `main.py`。
  * `app`: 指的是文件内实例化的 `app = FastAPI()` 对象。
  * `--reload`: 代码修改后自动重启服务器（仅开发模式使用）。

**访问交互式文档：**

FastAPI 的最大亮点是自动生成的交互式文档。启动成功后，在浏览器打开：

> **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**

-----

### 5\. 示例请求数据

测试 `POST` (创建) 接口时，可以使用以下 JSON 格式：

```json
{
  "title": "学习 FastAPI",
  "description": "阅读官方文档并完成 Hello World",
  "is_completed": false
}
```

-----