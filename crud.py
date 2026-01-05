from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, func
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
import models
import schemas

# --- 客房类型 (RoomType) 相关操作 ---

def get_room_types(db: Session):
    """
    获取数据库中所有的客房类型列表
    """
    return db.query(models.RoomType).all()

def create_room_type(db: Session, room_type: schemas.RoomTypeCreate):
    """
    创建并保存一个新的客房类型
    :param db: 数据库会话
    :param room_type: 客房类型创建模型
    """
    db_room_type = models.RoomType(**room_type.model_dump())
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type

# --- 客房信息 (RoomInfo) 相关操作 ---

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    """
    获取客房信息列表，支持分页，使用 joinedload 预加载房型信息并去重
    :param skip: 跳过的记录数
    :param limit: 返回的最大记录数
    """
    return db.query(models.RoomInfo)\
        .options(joinedload(models.RoomInfo.roomType))\
        .distinct()\
        .order_by(models.RoomInfo.roomNo)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_room(db: Session, room: schemas.RoomInfoCreate):
    """
    录入新的客房基本信息
    :param room: 客房信息创建模型
    """
    db_room = models.RoomInfo(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room_status_stats(db: Session):
    """
    获取实时房态统计数据
    """
    total = db.query(models.RoomInfo).count()
    free = db.query(models.RoomInfo).filter(models.RoomInfo.roomStatus == "空闲").count()
    occupied = db.query(models.RoomInfo).filter(models.RoomInfo.roomStatus == "已入住").count()
    return {"total": total, "free": free, "occupied": occupied}

# --- 宾客信息 (GuestInfo) 相关操作 ---

def get_guests(db: Session, skip: int = 0, limit: int = 100):
    """
    获取宾客入住记录列表，支持分页，并关联查询房型价格
    使用 outerjoin 确保即使房间信息不匹配也能返回记录，并处理 CHAR 类型的空格
    """
    results = db.query(
        models.GuestInfo,
        models.RoomType.roomPrice
    ).outerjoin(
        models.RoomInfo, func.rtrim(models.GuestInfo.roomNo) == func.rtrim(models.RoomInfo.roomNo)
    ).outerjoin(
        models.RoomType, models.RoomInfo.roomTypeId == models.RoomType.roomTypeId
    ).order_by(models.GuestInfo.guestId.desc())\
     .offset(skip).limit(limit).all()
    
    guest_list = []
    for guest, price in results:
        guest_obj = guest
        # 如果没有匹配到价格，默认为 0
        guest_obj.roomPrice = float(price) if price else 0.0
        guest_list.append(guest_obj)
        
    return guest_list

def create_guest(db: Session, guest: schemas.GuestInfoCreate):
    """
    办理宾客入住登记，保存入住信息
    :param guest: 宾客入住信息模型
    """
    try:
        # 确保 roomNo 没有任何多余空格
        guest_data = guest.model_dump()
        if guest_data.get('roomNo'):
            guest_data['roomNo'] = guest_data['roomNo'].strip()
            
        db_guest = models.GuestInfo(**guest_data)
        db.add(db_guest)
        db.commit()
        db.refresh(db_guest)
        return db_guest
    except IntegrityError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e

def update_guest_checkout(db: Session, guest_id: int, checkout_time: datetime):
    """
    办理宾客退房手续，更新退房时间
    :param guest_id: 宾客ID
    :param checkout_time: 退房日期时间
    """
    db_guest = db.query(models.GuestInfo).filter(models.GuestInfo.guestId == guest_id).first()
    if db_guest:
        db_guest.checkOutTime = checkout_time
        db.commit()
        db.refresh(db_guest)
    return db_guest

# --- 存储过程和视图 (高级业务查询) ---

def search_free_rooms_by_type(db: Session, room_type_name: str):
    """
    调用存储过程 proc_searchFreeRoomByTypeName
    根据客房类型名称查询当前所有空闲的房间
    """
    sql = text("EXEC proc_searchFreeRoomByTypeName @roomTypeName=:name")
    result = db.execute(sql, {"name": room_type_name})
    return result.mappings().all()

def search_guest_info_by_keyword(db: Session, keyword: str):
    """
    调用存储过程 proc_searchGuestInfoByKeyword
    通过关键字（姓名、房号或身份证号）模糊查询宾客详细信息
    """
    sql = text("EXEC proc_searchGuestInfoByKeyword @searchKey=:key")
    result = db.execute(sql, {"key": keyword})
    return result.mappings().all()

def get_room_occupancy_rate(db: Session, start_date: date, end_date: date):
    """
    调用存储过程 proc_statisticsRoomOccupancyRate
    统计指定日期范围内的各类客房出租率
    """
    sql = text("EXEC proc_statisticsRoomOccupancyRate @startDate=:start, @endDate=:end")
    result = db.execute(sql, {"start": start_date, "end": end_date})
    return result.mappings().all()

def get_annual_revenue(db: Session, year: int):
    """
    调用存储过程 proc_statisticsAnnualRevenue
    统计指定年份各月份的客房收入
    """
    sql = text("EXEC proc_statisticsAnnualRevenue @year=:year")
    result = db.execute(sql, {"year": year})
    return result.mappings().all()

def get_guest_cost_detail(db: Session, guest_id: int):
    """
    调用存储过程 proc_searchGuestCostDetail
    查询指定宾客的消费明细，包括实住天数、应收费用及退还押金等（用于结算）
    """
    sql = text("EXEC proc_searchGuestCostDetail @guestId=:id")
    result = db.execute(sql, {"id": guest_id})
    return result.mappings().first()

def get_expired_stay_guests(db: Session):
    """
    查询视图 view_expiredStayGuest
    获取当前所有已经超过预计入住天数但尚未退房的宾客列表
    """
    sql = text("SELECT * FROM view_expiredStayGuest")
    result = db.execute(sql)
    return result.mappings().all()
