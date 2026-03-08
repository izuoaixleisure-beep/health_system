from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user
from .. import models

router = APIRouter(
    prefix="/residents",
    tags=["Residents"]
)


def _require_doctor(current_user):
    """仅医生可执行，否则 403"""
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="仅医生可执行此操作")


# 查询居民：居民只能查自己，医生可分页查全部
@router.get("/", response_model=list[schemas.ResidentResponse])
async def read_residents(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role == "resident":
        if current_user.resident_id is None:
            return []
        r = crud.get_resident_by_id(db, current_user.resident_id)
        return [r] if r else []
    _require_doctor(current_user)
    skip = (page - 1) * limit
    return crud.get_residents(db, skip, limit)


# 根据 id 查询单条居民（仅医生）
@router.get("/{resident_id}", response_model=schemas.ResidentResponse)
async def read_resident_by_id(
    resident_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    _require_doctor(current_user)
    r = crud.get_resident_by_id(db, resident_id)
    if not r:
        raise HTTPException(status_code=404, detail="居民不存在")
    return r


# 修改居民（仅医生）
@router.put("/{resident_id}", response_model=schemas.ResidentResponse)
async def update_resident(
    resident_id: int,
    resident: schemas.ResidentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    _require_doctor(current_user)
    updated = crud.update_resident(db, resident_id, resident)
    if not updated:
        raise HTTPException(status_code=404, detail="居民不存在")
    return updated


# 删除居民（仅医生）
@router.delete("/{resident_id}")
async def delete_resident(
    resident_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    _require_doctor(current_user)
    if not crud.delete_resident(db, resident_id):   #调用并判断一步写
        raise HTTPException(status_code=404, detail="居民不存在")
    return {"message": "删除成功"}
