# intimoi Backend

intimoi 小程序后端服务，基于 FastAPI + SQLAlchemy + MySQL。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入真实配置
```

### 3. 初始化数据库

```bash
python scripts/init_db.py --with-sample-data
```

### 4. 启动服务

```bash
python main.py
# 或者
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API 文档

启动服务后访问: http://localhost:8000/docs

## 项目结构

```
backend/
├── app/
│   ├── api/v1/         # API 路由
│   ├── models/         # SQLAlchemy 模型
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # 业务服务（WeChat, WDT）
│   ├── middleware/     # 中间件（JWT认证）
│   └── utils/          # 工具函数
├── tests/              # 单元测试
├── scripts/            # 初始化脚本
└── main.py            # 入口
```

## 运行测试

```bash
pytest tests/ -v
```
