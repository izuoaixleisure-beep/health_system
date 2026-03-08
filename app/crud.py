from sqlalchemy.orm import Session
from . import models, schemas
from .auth import verify_password, hash_password

# 注册：创建用户（密码已哈希，带 role）
def create_user(db: Session, username: str, hashed_password: str, role: str, resident_id: int | None = None):
    db_user = models.User(
        username=username,
        password=hashed_password,
        role=role,
        resident_id=resident_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 注册医生
def register_doctor(db: Session, req: schemas.RegisterRequest):
    if get_user_by_username(db, req.username):
        return None, "用户名已存在"
    create_user(db, req.username, hash_password(req.password), req.role.value, resident_id=None)
    return get_user_by_username(db, req.username), None

# 注册居民：先创建 Resident，再创建 User 并关联 resident_id
def register_resident(db: Session, req: schemas.RegisterRequest):
    if get_user_by_username(db, req.username):
        return None, "用户名已存在"
    resident = models.Resident(
        name=req.name,
        gender=req.gender,
        birth_date=req.birth_date,
        phone=req.phone,
        address=req.address
    )
    db.add(resident)
    db.commit()
    db.refresh(resident)
    create_user(db, req.username, hash_password(req.password), req.role.value, resident_id=resident.id)
    return get_user_by_username(db, req.username), None

# 查询用户
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()

# 根据 id 查询单个居民
def get_resident_by_id(db: Session, resident_id: int):
    return db.query(models.Resident).filter(models.Resident.id == resident_id).first()

#查询所有居民
def get_residents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Resident).offset(skip).limit(limit).all()

#修改居民
def update_resident(db: Session, resident_id: int, resident: schemas.ResidentUpdate):
    db_resident = db.query(models.Resident).filter(models.Resident.id == resident_id).first()
    if not db_resident:
        return None
    db_resident.name = resident.name
    db_resident.gender = resident.gender
    db_resident.birth_date = resident.birth_date
    db_resident.phone = resident.phone
    db_resident.address = resident.address
    db.commit()
    db.refresh(db_resident)
    return db_resident

# 创建健康记录
def create_health(db: Session, health: schemas.HealthCreate):
    db_health = models.Health(
        resident_id=health.resident_id,
        checkup_date=health.checkup_date,
        height=health.height,
        weight=health.weight,
        diseases=health.diseases or ""
    )
    db.add(db_health)
    db.commit()
    db.refresh(db_health)
    return db_health

# 根据 resident_id 查询该居民的健康记录（分页，按体检时间倒序）
def get_health_by_resident_id(db: Session, resident_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Health)
        .filter(models.Health.resident_id == resident_id)
        .order_by(models.Health.checkup_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

# 根据 id 查询单条健康记录
def get_health_by_id(db: Session, health_id: int):
    return db.query(models.Health).filter(models.Health.id == health_id).first()

# 分页查询所有健康记录（按体检时间倒序）
def get_health_records(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Health)
        .order_by(models.Health.checkup_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

# 修改健康记录
def update_health(db: Session, health_id: int, health: schemas.HealthUpdate):
    db_health = db.query(models.Health).filter(models.Health.id == health_id).first()
    if not db_health:
        return None
    if health.checkup_date is not None:
        db_health.checkup_date = health.checkup_date
    if health.height is not None:
        db_health.height = health.height
    if health.weight is not None:
        db_health.weight = health.weight
    if health.diseases is not None:
        db_health.diseases = health.diseases
    db.commit()
    db.refresh(db_health)
    return db_health

# 删除健康记录
def delete_health(db: Session, health_id: int):
    db_health = db.query(models.Health).filter(models.Health.id == health_id).first()
    if not db_health:
        return None
    db.delete(db_health)
    db.commit()
    return db_health

# 删除居民（同时删除关联的用户和健康记录）
def delete_resident(db: Session, resident_id: int):
    db_resident = db.query(models.Resident).filter(models.Resident.id == resident_id).first()
    if not db_resident:
        return None
    db.query(models.Health).filter(models.Health.resident_id == resident_id).delete()
    db.query(models.User).filter(models.User.resident_id == resident_id).delete()
    db.delete(db_resident)
    db.commit()
    return db_resident

# 删除用户（若为居民则同时删除关联的居民和健康记录）
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    if db_user.resident_id is not None:
        db.query(models.Health).filter(models.Health.resident_id == db_user.resident_id).delete()
        db.query(models.Resident).filter(models.Resident.id == db_user.resident_id).delete()
    db.delete(db_user)
    db.commit()
    return db_user

# 登录
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:    #没有用户
        return None
    if not verify_password(password, user.password):
        return None     #密码验证不通过
    return user