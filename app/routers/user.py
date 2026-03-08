from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth import create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# 注册
@router.post("/register")
async def register(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    if req.role == schemas.RoleEnum.doctor:
        user, err = crud.register_doctor(db, req)
    else:
        user, err = crud.register_resident(db, req)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return {"message": "注册成功", "username": user.username}

# 登录
@router.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="用户名不存在或密码错误")
    access_token = create_access_token(
        data={
            "sub": db_user.username,
            "role": db_user.role,
            "resident_id": db_user.resident_id
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 删除用户（仅医生；若为居民则同时删除关联的居民和健康记录）
@router.delete("/{user_id}")
async def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="仅医生可执行此操作")
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "删除成功"}