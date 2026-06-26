# Development Log

本文件记录 AI Learning Assistant Backend 的主要开发过程。

该项目从最基础的 FastAPI 文件上传开始，逐步加入大模型调用、模块化拆分、数据库持久化、历史查询、输入校验和异常处理。当前目标是将项目从普通 AI 总结工具，逐步升级为面向后端编程学习的 AI 知识库系统。

---

## V0.1 - 文件上传功能

### 目标

搭建 FastAPI 服务，实现 `.txt` 文件上传和内容读取。

### 完成内容

* 创建 FastAPI 应用
* 使用 Uvicorn 启动服务
* 使用 `UploadFile` 接收用户上传文件
* 使用 `File(...)` 声明文件上传参数
* 读取文件内容并返回
* 初步处理 UTF-8 / GBK 编码问题

### 涉及技术

* FastAPI
* Uvicorn
* UploadFile
* File
* async / await
* 文件编码处理

### 踩坑与修正

部分 Windows 文本文件不是 UTF-8 编码，直接 decode 会报错。

解决方式：

* 优先尝试 UTF-8
* 失败后尝试 GBK
* 后续版本扩展为多编码检测

### 当前成果

项目完成了最基础的文件上传链路：

```text
浏览器 / Swagger
↓
Uvicorn
↓
FastAPI
↓
UploadFile
↓
read()
↓
bytes
↓
decode
↓
str
```

---

## V0.2 - 接入 DeepSeek 总结功能

### 目标

在文件上传成功后，调用 DeepSeek API 对文本内容进行总结。

### 完成内容

* 使用 `.env` 保存 API Key
* 使用 `python-dotenv` 加载环境变量
* 使用 OpenAI Python SDK 调用 DeepSeek API
* 构造总结类 Prompt
* 返回模型生成结果

### 涉及技术

* OpenAI Python SDK
* DeepSeek API
* dotenv
* 环境变量
* Prompt 设计
* try / except
* raise

### 踩坑与修正

最初 API Key 读取失败，原因是 `.env` 加载路径和环境变量名称没有理清。

修正后，将敏感配置放入 `.env`，避免直接写死在代码中。

### 当前成果

完成基础 AI 调用链路：

```text
上传文件
↓
读取文本
↓
构造 Prompt
↓
调用 DeepSeek
↓
返回总结
```

---

## V0.3 - 项目模块化重构

### 目标

将原本集中在 `main.py` 中的代码拆分为不同模块，提升可维护性。

### 完成内容

* 拆分 AI 调用逻辑
* 拆分总结、面试题、学习计划功能
* 新增多个接口：

  * `POST /summarize`
  * `POST /question`
  * `POST /study_plan`
* 初步形成路由层和服务层分离

### 涉及技术

* Python 模块导入
* FastAPI 路由
* service 层
* Prompt 复用
* 项目结构设计

### 踩坑与修正

最初对 `main.py` 的职责理解不清，容易把所有业务代码都放进入口文件。

修正后：

* `main.py` 负责接收请求和调用服务
* AI 服务模块负责调用模型和组织 Prompt
* 工具函数后续抽离到 `utils.py`

### 当前成果

项目从单文件脚本开始转向分层结构：

```text
main.py
↓
service_ai.py
↓
DeepSeek API
```

---

## V0.4 - 接入 SQLAlchemy 数据库

### 目标

为项目加入数据库持久化能力，保存 AI 任务执行记录。

### 完成内容

* 使用 SQLAlchemy 创建数据库连接
* 使用 SQLite 作为开发阶段数据库
* 定义 ORM 模型 `AIRecord`
* 创建数据库表
* 实现 AI 结果保存函数
* 理解 Session、commit、refresh、rollback 的作用

### 数据模型

当前核心表为 `ai_records`：

* `id`
* `filename`
* `task_type`
* `result`
* `create_at`

### 涉及技术

* SQLAlchemy
* SQLite
* ORM
* Engine
* SessionLocal
* Session
* commit
* refresh
* rollback

### 踩坑与修正

需要区分：

* Engine 是数据库访问入口，不是单个连接
* Session 是一次数据库操作的事务管理对象，不适合全局共享
* `create_engine()` 不负责建表
* `Base.metadata.create_all(bind=engine)` 才负责根据 ORM 模型创建表
* `commit()` 失败后需要 `rollback()`

### 当前成果

项目从“AI 处理后直接返回”升级为：

```text
上传文件
↓
AI 处理
↓
保存数据库
↓
返回记录 ID 和结果
```

---

## V0.5 - 数据库查询与项目结构优化

### 目标

完善数据库查询能力，并进一步拆分项目结构。

### 完成内容

* 将工具函数拆分到 `utils.py`
* 实现历史记录查询接口
* 实现单条记录详情接口
* 修正 `/record/{record_id}` 返回结构
* 修正数据库查询结果不需要再次 decode 的问题
* 为数据库写入增加 rollback
* 初步加入文件名安全处理思路

### 当前接口

* `GET /health`
* `POST /summarize`
* `POST /question`
* `POST /study_plan`
* `GET /records`
* `GET /record/{record_id}`

### 项目结构

```text
main.py          # 路由层
utils.py         # 工具函数层
database.py      # 数据库层
service_ai.py    # AI 服务层
```

### 踩坑与修正

#### 1. 数据库中的 result 不需要再次 decode

上传文件时，`file.read()` 得到的是 bytes，需要 decode。

但数据库 `Text` 字段读取出来后通常已经是 str，因此不能再传给编码检测函数。

错误方式：

```python
detection_coding(record.result)
```

正确方式：

```python
record.result
```

#### 2. 单条记录接口不应返回列表

查询单条记录时，应返回 dict，而不是只包含一个 dict 的 list。

#### 3. 查询空列表不应返回 404

`GET /records` 如果没有数据，返回 `[]` 更合理。

### 当前成果

项目完成了较完整的后端基础闭环：

```text
上传 → AI处理 → 数据库存储 → 历史查询 → 单条详情查询
```

---

## V0.6 - 输入校验与 AI 调用防御

### 目标

提高接口稳定性，减少无效输入和无效 AI 调用。

### 完成内容

* 新增自定义文件校验异常
* 新增上传文本数据结构
* 文件名安全处理
* 多编码检测
* 文本长度校验
* 空文本拒绝
* 过短文本拒绝
* 超长文本拒绝
* DeepSeek API timeout
* API 连接错误处理
* API 超时处理
* API 限流错误处理
* 简单重试机制
* 空响应检测

### 涉及技术

* dataclass
* 自定义异常
* FastAPI exception_handler
* JSONResponse
* 多编码 fallback
* API timeout
* retry
* RuntimeError

### 当前输入校验

当前支持：

* 文件名不能为空
* 仅允许 `.txt` 文件
* 清洗上传文件名，避免路径污染
* 尝试多种常见编码
* 文本不能为空
* 文本不能过短
* 文本不能超长
* 超过推荐长度时给出截断警告

### 当前 AI 调用防御

DeepSeek API 调用支持：

* timeout
* 最多重试
* 连接错误捕获
* 超时错误捕获
* 限流错误捕获
* 空 choices 检测
* 空 content 检测

### 当前成果

项目从“功能能跑”进一步升级为“具备基础防御性编程能力”的后端服务。

---

## 当前项目能力

目前已经完成：

* FastAPI 服务搭建
* 文件上传
* 文本读取
* 多编码检测
* 文件名安全处理
* 文本长度校验
* DeepSeek API 调用
* AI 总结
* AI 面试题生成
* AI 学习计划生成
* SQLAlchemy ORM
* SQLite 数据持久化
* 历史记录查询
* 单条记录查询
* AI 调用错误处理
* 项目模块化拆分

---

## 当前限制

当前项目仍处于学习阶段，尚未完成：

* content_hash 去重
* documents 表
* RAG 检索
* 学习路径 Agent
* 用户系统
* JWT
* Redis
* 单元测试
* 部署
* PostgreSQL 迁移

---

## 后续规划

### V0.7 - 文档资源化

计划新增：

* `documents` 表
* 原始文本保存
* `content_hash` 去重
* `ai_records` 关联 `document_id`

目标是将上传文件从一次性输入升级为可管理的知识库资源。

---

### V0.8 - 轻量 RAG 问答

计划新增：

* `POST /ask`
* 基于历史资料的关键词检索
* 将检索结果拼接进 Prompt
* 返回基于用户资料的回答

目标是实现最小版 RAG：

```text
Retrieve → Augment → Generate
```

---

### V0.9 - 学习路径 Agent

计划新增：

* `POST /learning-path`
* 根据学习目标检索历史资料
* 生成阶段性学习路线
* 生成每日任务
* 生成自测题

目标是实现一个面向后端编程学习的轻量任务编排 Agent。

---

### V1.0 - 项目包装

计划补充：

* README 完善
* requirements.txt
* `.env.example`
* 基础测试
* 接口文档
* 项目架构图
* 部署说明

---

## 项目定位

本项目不是通用聊天机器人，而是一个面向后端编程学习场景的 AI 学习资料处理系统。

当前核心目标：

```text
文件上传
↓
AI 处理
↓
数据库保存
↓
历史查询
↓
知识库化
↓
轻量 RAG
↓
学习路径 Agent
```
