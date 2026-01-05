from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import crud
import schemas
from database import get_db

router = APIRouter()

# --- 宾客入住接口 ---

@router.get("/", response_model=List[schemas.GuestInfo], tags=["宾客管理"])
def read_guests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取宾客列表"""
    return crud.get_guests(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.GuestInfo, tags=["宾客管理"])
def create_guest(guest: schemas.GuestInfoCreate, db: Session = Depends(get_db)):
    """登记宾客入住"""
    try:
        return crud.create_guest(db=db, guest=guest)
    except Exception as e:
        print(f"创建宾客失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建宾客失败: {str(e)}")

@router.post("/{guest_id}/checkout", response_model=schemas.GuestInfo, tags=["宾客管理"])
def checkout_guest(guest_id: int, db: Session = Depends(get_db)):
    """办理退房手续"""
    checkout_time = datetime.now()
    db_guest = crud.update_guest_checkout(db, guest_id=guest_id, checkout_time=checkout_time)
    if db_guest is None:
        raise HTTPException(status_code=404, detail="未找到该宾客记录")
    return db_guest
