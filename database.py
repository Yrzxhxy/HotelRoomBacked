from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_SERVER = os.getenv("DB_SERVER", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Abc@12345678")
DB_NAME = os.getenv("DB_NAME", "hotelRoomManageDb")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

# 构造连接字符串
params = urllib.parse.quote_plus(
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# 创建引擎和会话
# implicit_returning=False 解决 SQL Server 触发器与 OUTPUT 子句的冲突
engine = create_engine(SQLALCHEMY_DATABASE_URL, implicit_returning=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 获取数据库会话的依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
