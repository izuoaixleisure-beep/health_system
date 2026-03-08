from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/health", tags=["Health"])


def _require_doctor(current_user):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="仅医生可执行此操作")


# 创建健康记录（仅医生）
@router.post("/", response_model=schemas.HealthResponse)
async def create_health(
    health: schemas.HealthCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    _require_doctor(current_user)
    if not crud.get_resident_by_id(db, health.resident_id):
        raise HTTPException(status_code=404, detail="居民不存在")
    return crud.create_health(db, health)


# 查询健康记录：居民和医生都可访问，均支持分页，按体检时间倒序
@router.get("/", response_model=list[schemas.HealthResponse])
async def read_health(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    skip = (page - 1) * limit
    if current_user.role == "resident":
        if current_user.resident_id is None:
            return []
        return crud.get_health_by_resident_id(db, current_user.resident_id, skip, limit)
    return crud.get_health_records(db, skip, limit)


# 根据 id 查询单条健康记录（仅医生）
@router.get("/{health_id}", response_model=schemas.HealthResponse)
async def read_health_by_id(
    health_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    _require_doctor(current_user)
    h = crud.get_health_by_id(db, health_id)
    if not h:
        raise HTTPException(status_code=404, detail="健康记录不存在")
    return h


# 修改健康记录（仅医生）
@router.put("/{health_id}", response_model=schemas.HealthResponse)
async def update_health(
    health_id: int,
    health: schemas.HealthUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    _require_doctor(current_user)
    updated = crud.update_health(db, health_id, health)
    if not updated:
        raise HTTPException(status_code=404, detail="健康记录不存在")
    return updated


# 删除健康记录（仅医生）
@router.delete("/{health_id}")
async def delete_health(
    health_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    _require_doctor(current_user)
    if not crud.delete_health(db, health_id):
        raise HTTPException(status_code=404, detail="健康记录不存在")
    return {"message": "删除成功"}
