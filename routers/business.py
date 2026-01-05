from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Any
from datetime import datetime, date
import crud
import schemas
from database import get_db

router = APIRouter()

# --- 业务查询与统计接口 (调用存储过程/视图) ---

@router.get("/search/free-rooms", response_model=List[schemas.FreeRoomSearch], tags=["业务功能"])
def search_free_rooms(room_type_name: str, db: Session = Depends(get_db)):
    """根据房型查询空闲房间"""
    return crud.search_free_rooms_by_type(db, room_type_name=room_type_name)

@router.get("/search/guests", response_model=List[schemas.GuestSearchExtended], tags=["业务功能"])
def search_guests(keyword: str, db: Session = Depends(get_db)):
    """根据姓名/房号/身份证查询宾客"""
    return crud.search_guest_info_by_keyword(db, keyword=keyword)

@router.get("/statistics/occupancy-rate", response_model=List[schemas.RoomOccupancyRate], tags=["统计报表"])
def get_occupancy_rate(
    start_date: date = Query(..., description="开始日期 (YYYY-MM-DD)"),
    end_date: date = Query(..., description="结束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """统计客房出租率"""
    return crud.get_room_occupancy_rate(db, start_date=start_date, end_date=end_date)

@router.get("/statistics/annual-revenue", response_model=List[schemas.AnnualRevenue], tags=["统计报表"])
def get_annual_revenue(
    year: int = Query(..., description="年份 (如 2024)"),
    db: Session = Depends(get_db)
):
    """统计年度月度收入"""
    return crud.get_annual_revenue(db, year=year)

@router.get("/cost-detail/{guest_id}", response_model=schemas.GuestCostDetail, tags=["业务功能"])
def get_cost_detail(guest_id: int, db: Session = Depends(get_db)):
    """查询宾客退房结算详情"""
    detail = crud.get_guest_cost_detail(db, guest_id=guest_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="未找到消费详情")
    return detail

@router.get("/guests/expired-stays", response_model=List[Any], tags=["业务功能"])
def get_expired_guests(db: Session = Depends(get_db)):
    """查询超期未退房的宾客"""
    return crud.get_expired_stay_guests(db)
