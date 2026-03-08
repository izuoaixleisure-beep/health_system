from pydantic import BaseModel, model_validator
from datetime import date
from enum import Enum

# 角色枚举：只允许 doctor 和 resident
class RoleEnum(str, Enum):
    doctor = "doctor"
    resident = "resident"

#接口参数模型
# 登录用模型
class UserLogin(BaseModel):
    username: str
    password: str

# 注册请求：医生只需 username/password/role，居民还需居民信息
class RegisterRequest(BaseModel):
    username: str
    password: str
    role: RoleEnum
    # 以下仅 role=resident 时必填
    name: str | None = None
    gender: str | None = None
    birth_date: date | None = None
    phone: str | None = None
    address: str | None = None

    @model_validator(mode="after")
    def check_resident_fields(self):
        if self.role == RoleEnum.resident and any(
            x is None for x in [self.name, self.gender, self.birth_date, self.phone, self.address]
        ):
            raise ValueError("居民注册时必须填写 name, gender, birth_date, phone, address")
        return self

# 医生修改居民时使用的模型
class ResidentUpdate(BaseModel):
    name: str
    gender: str
    birth_date: date
    phone: str
    address: str

# 健康记录创建模型
class HealthCreate(BaseModel):
    resident_id: int
    checkup_date: date   # 体检时间
    height: float
    weight: float
    diseases: str = ""

# 健康记录修改模型
class HealthUpdate(BaseModel):
    checkup_date: date | None = None
    height: float | None = None
    weight: float | None = None
    diseases: str | None = None

# 健康记录返回模型
class HealthResponse(BaseModel):
    id: int
    resident_id: int
    checkup_date: date
    height: float
    weight: float
    diseases: str
    class Config:
        from_attributes = True

# 居民数据返回前端模型
class ResidentResponse(BaseModel):
    id: int
    name: str
    gender: str
    birth_date: date
    phone: str
    address: str
#允许 Pydantic 读取 ORM 对象
    class Config:
        from_attributes = True
