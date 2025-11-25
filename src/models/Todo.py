# -*- coding: utf-8 -*-
# @Author  : sxw
# @Time    : 2025/11/25 11:32
# @Desc    : 数据模型
from pydantic import BaseModel
from typing import Optional

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