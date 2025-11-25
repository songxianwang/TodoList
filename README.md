**FastAPI** 的简易待办事项（Todo List）API ，旨在快速构建一个具备 **CRUD**（增删改查）功能的后端服务。

-----

### 1\. 环境准备

首先，确保已经安装了 Python，然后安装 FastAPI 和 ASGI 服务器（Uvicorn）：

```bash
pip install fastapi uvicorn
```

-----

### 2\. 代码解析

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

### 3\. 如何运行与测试

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

### 4\. 示例请求数据

测试 `POST` (创建) 接口时，可以使用以下 JSON 格式：

```json
{
  "title": "学习 FastAPI",
  "description": "阅读官方文档并完成 Hello World",
  "is_completed": false
}
```

-----