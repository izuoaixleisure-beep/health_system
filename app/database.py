import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 从环境变量读取数据库连接，提供默认值（兼容本地开发）
# 原因：Docker 容器中通过环境变量注入配置，本地开发可以用默认值
# 容器内 mysql 是服务名，Docker 会自动解析为容器 IP
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:wxsadc421@localhost/health_db"
)

# 创建引擎，pool_pre_ping=True 检测连接是否有效
# 原因：MySQL 有连接超时，长时间不用会断开，pool_pre_ping 自动重连
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
