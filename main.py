from fastapi import FastAPI
from src.urls.todo_url import todo_app

app = FastAPI(
    title="简易待办事项 API",
    description="FastAPI => Todo List",
    version="1.0.0"
)

@app.get("/",tags=["介绍项目"])
async def read_root():
    return {"message": "欢迎使用 Todo API! 请访问 /docs 查看文档。"}

app.include_router(todo_app, prefix="/todo", tags=["代办接口"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)