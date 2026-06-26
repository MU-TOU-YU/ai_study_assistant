# AI Learning Assistant Backend

基于 FastAPI、SQLAlchemy 和 DeepSeek API 实现的 AI 学习资料处理后端项目。

当前版本支持用户上传 `.txt` 学习资料，并自动生成：

* 学习资料总结
* 面试题与参考答案
* 阶段性学习计划
* 历史任务记录查询
* 单条任务详情查询

该项目是一个面向后端编程学习场景的 AI 应用后端雏形，后续计划扩展为「后端学习知识库 + 轻量 RAG 问答 + 学习路径 Agent」。

---

## 项目背景

本项目最初用于练习 FastAPI 后端开发流程。

项目从最基础的文件上传开始，逐步加入：

* 文件读取与编码处理
* DeepSeek API 调用
* Prompt 设计
* SQLAlchemy 数据库存储
* 历史记录查询
* 输入校验与异常处理
* 项目模块化拆分

当前目标不是构建完整商业产品，而是通过一个真实可运行的小项目，理解 Python 后端开发中的核心流程。

---

## 当前功能

### 1. 健康检查

```http
GET /health
```

用于确认服务是否正常启动。

---

### 2. 上传文本并生成总结

```http
POST /summarize
```

上传 `.txt` 文件后，系统会读取文本内容，调用 DeepSeek API 生成学习资料总结，并将结果保存到数据库。

---

### 3. 上传文本并生成面试题

```http
POST /question
```

根据上传资料生成 5 道由浅入深的面试题，并附带参考答案。

---

### 4. 上传文本并生成学习计划

```http
POST /study_plan
```

根据上传资料生成适合初学者的阶段性学习计划。

---

### 5. 查询历史记录

```http
GET /records
```

查询所有 AI 任务记录。

---

### 6. 查询单条记录

```http
GET /record/{record_id}
```

根据记录 id 查询某次 AI 任务的完整结果。

---

## 技术栈

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* DeepSeek API
* OpenAI Python SDK
* python-dotenv

---

## 项目结构

```text
project/
├── main.py              # FastAPI 应用入口与路由层
├── database.py          # SQLAlchemy 数据库模型与 CRUD 函数
├── utils.py             # 文件上传、编码检测、输入校验、响应构造
├── service/
│   └── service_ai.py    # DeepSeek API 调用与 Prompt 逻辑
├── docs/
│   └── dev-log.md       # 项目学习与迭代日志
├── requirements.txt
├── .env.example
└── README.md
```

---

## 核心流程

```text
用户上传 txt 文件
↓
FastAPI 路由接收请求
↓
UploadFile 读取文件内容
↓
编码检测与文本校验
↓
调用 DeepSeek API
↓
生成总结 / 面试题 / 学习计划
↓
SQLAlchemy 保存数据库记录
↓
返回统一 JSON 响应
```

---

## 数据库设计

当前使用 SQLite 作为学习阶段数据库。

核心表：`ai_records`

字段包括：

* `id`：记录主键
* `filename`：上传文件名
* `task_type`：任务类型，例如 summary、question、study_plan
* `result`：AI 生成结果
* `create_at`：创建时间

---

## 输入校验

当前已支持：

* 仅允许上传 `.txt` 文件
* 文件名安全处理
* 多编码尝试解码
* 文本长度校验
* 空文本拒绝
* 过短文本拒绝
* 超长文本拒绝

---

## AI 调用处理

DeepSeek API 调用已加入基础防御：

* timeout 设置
* API 连接错误处理
* API 超时处理
* 限流错误处理
* 简单重试机制
* 空响应检测

---

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd <your-project-name>
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
```

macOS / Linux：

```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

在 `.env` 中填写：

```env
DeepSeek_API_KEY=your_api_key_here
```

### 5. 启动服务

```bash
uvicorn main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/docs
```

可以在 Swagger 页面测试接口。

---

## 示例响应

```json
{
  "id": 1,
  "filename": "python_note.txt",
  "task_type": "summarize",
  "result": "这份资料主要讲解了..."
}
```


## 项目定位

本项目不是通用聊天机器人，而是一个面向后端编程学习场景的 AI 知识处理后端。

当前重点是：

* 掌握 FastAPI 后端开发流程
* 理解文件上传与 HTTP 请求处理
* 理解 SQLAlchemy ORM 与数据库持久化
* 理解 AI API 调用与异常处理
* 为后续 RAG 和 Agent 功能打基础
