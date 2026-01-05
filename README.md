# 酒店客房管理系统 - 后端

本项目是基于 FastAPI 和 SQL Server 构建的酒店管理系统后端 API。

## 技术栈

- **框架**: [FastAPI](https://fastapi.tiangolo.com/)
- **数据库**: Microsoft SQL Server
- **ORM**: SQLAlchemy
- **数据验证**: Pydantic
- **运行环境**: Python 3.11+

## 目录结构

```text
backed/
├── routers/          # 路由模块 (rooms, guests, business)
├── crud.py           # 数据库增删改查逻辑
├── database.py       # 数据库连接配置
├── main.py           # 程序入口
├── models.py         # 数据库模型 (SQLAlchemy)
├── schemas.py        # 数据验证模型 (Pydantic)
├── .env              # 环境配置 (数据库连接字符串等)
└── requirements.txt  # 依赖项列表
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

在 `.env` 文件中配置您的 SQL Server 连接字符串：

```env
DATABASE_URL=mssql+pyodbc://username:password@localhost/HotelRoomManageDB?driver=ODBC+Driver+17+for+SQL+Server
```

### 3. 运行服务

```bash
python main.py
```

服务启动后，可以通过以下地址访问：
- API 首页: `http://localhost:8000/`
- 交互式文档 (Swagger UI): `http://localhost:8000/docs`

## 主要功能

- **客房管理**: 房型定义、房间增删改查、房态实时监控。
- **宾客管理**: 宾客信息登记、搜索、后端自动化脱敏展示逻辑支持。
- **业务逻辑**: 办理入住、退房结算处理、费用明细计算。
- **数据分析**: 调用存储过程实现各类房型出租率、年度/月度收入、实时房态等统计接口。

## 数据安全性

本项目采用后端脱敏方案：
- **手机号脱敏**: `138****8888` (保留前3后4)
- **身份证脱敏**: `110101********1234` (保留前6后4)
脱敏逻辑集成在 Pydantic 响应模型中，确保敏感数据在离开服务器前已完成加密处理。
