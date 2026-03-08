from .database import Base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
# 数据库模型
#用户表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(200))
    role = Column(String(20))  # doctor / resident
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=True)

# 居民表
class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    gender = Column(String(10))
    birth_date = Column(Date)
    phone = Column(String(20))
    address = Column(String(200))


# 健康表（与居民一对多，一个居民可有多条体检记录）
class Health(Base):
    __tablename__ = "health"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    checkup_date = Column(Date)   # 体检时间
    height = Column(Float)        # 身高(cm)
    weight = Column(Float)        # 体重(kg)
    diseases = Column(Text)       # 疾病（可存多个，如逗号分隔）