from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter()

# --- 客房类型接口 ---

@router.get("/room-types/", response_model=List[schemas.RoomType], tags=["客房类型"])
def read_room_types(db: Session = Depends(get_db)):
    """获取所有客房类型"""
    return crud.get_room_types(db)

@router.post("/room-types/", response_model=schemas.RoomType, tags=["客房类型"])
def create_room_type(room_type: schemas.RoomTypeCreate, db: Session = Depends(get_db)):
    """创建新的客房类型"""
    return crud.create_room_type(db=db, room_type=room_type)

# --- 客房信息接口 ---

@router.get("/", response_model=List[schemas.RoomInfo], tags=["客房信息"])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取客房列表"""
    return crud.get_rooms(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.RoomInfo, tags=["客房信息"])
def create_room(room: schemas.RoomInfoCreate, db: Session = Depends(get_db)):
    """录入新的客房信息"""
    return crud.create_room(db=db, room=room)

@router.get("/stats/summary", response_model=schemas.RoomStatusStats, tags=["客房信息"])
def get_room_stats(db: Session = Depends(get_db)):
    """获取实时房态统计总结"""
    return crud.get_room_status_stats(db)
