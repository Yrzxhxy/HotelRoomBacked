from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- 客房类型 (RoomType) 模式 ---
class RoomTypeBase(BaseModel):
    """客房类型基础字段"""
    roomTypeId: str
    roomTypeName: str
    roomPrice: Decimal
    roomDesc: Optional[str] = None

class RoomTypeCreate(RoomTypeBase):
    """创建客房类型时的请求数据"""
    pass

class RoomType(RoomTypeBase):
    """返回给前端的客房类型数据"""
    class Config:
        from_attributes = True

# --- 客房信息 (RoomInfo) 模式 ---
class RoomInfoBase(BaseModel):
    """客房基础字段"""
    roomNo: str
    roomTypeId: str
    roomStatus: Optional[str] = "空闲"
    roomFloor: Optional[int] = None
    roomBedCount: Optional[int] = None

class RoomInfoCreate(RoomInfoBase):
    """创建客房时的请求数据"""
    pass

class RoomInfo(RoomInfoBase):
    """返回给前端的客房详细信息"""
    roomType: Optional[RoomType] = None
    class Config:
        from_attributes = True

# --- 宾客入住 (GuestInfo) 模式 ---
class GuestInfoBase(BaseModel):
    """宾客入住基础字段"""
    guestName: str
    guestGender: Optional[str] = "男"
    guestAge: Optional[int] = None
    idCard: str
    phoneNum: Optional[str] = None
    address: Optional[str] = None
    workplace: Optional[str] = None
    comeFrom: Optional[str] = None
    stayDays: int
    roomNo: Optional[str] = None
    depositMoney: Optional[Decimal] = 0.00
    remark: Optional[str] = None

class GuestInfoCreate(GuestInfoBase):
    """办理入住时的请求数据"""
    pass

class GuestInfoUpdate(BaseModel):
    """办理退房或更新信息时的请求数据"""
    checkOutTime: Optional[datetime] = None

class GuestInfo(GuestInfoBase):
    """返回给前端的宾客信息"""
    guestId: int
    checkInTime: datetime
    checkOutTime: Optional[datetime] = None
    roomCost: Decimal
    roomPrice: Optional[Decimal] = 0.00  # 新增：房型单价

    @field_validator('phoneNum')
    @classmethod
    def mask_phone(cls, v):
        if not v or len(v) != 11:
            return v
        return f"{v[:3]}****{v[7:]}"

    @field_validator('idCard')
    @classmethod
    def mask_id_card(cls, v):
        if not v:
            return ""
        length = len(v)
        if length < 10:
            return v
        return f"{v[:6]}{'*' * (length - 10)}{v[-4:]}"

    class Config:
        from_attributes = True

# --- 存储过程专用的自定义响应模式 ---

class FreeRoomSearch(BaseModel):
    """空闲客房查询结果 (存储过程: proc_GetFreeRooms)"""
    roomNo: str
    roomTypeName: str
    roomPrice: Decimal
    roomFloor: int
    roomBedCount: int

class GuestSearchExtended(GuestInfo):
    """包含房价信息的宾客查询结果 (存储过程: proc_GetGuestDetails)"""
    roomTypeName: str
    roomPrice: Decimal

class RoomOccupancyRate(BaseModel):
    """客房出租率统计 (存储过程: proc_GetRoomOccupancyRate)"""
    roomTypeName: str
    totalRoomCount: int
    occupiedRoomCount: int
    occupancyRate: Decimal

class RoomStatusStats(BaseModel):
    """实时房态统计"""
    total: int
    free: int
    occupied: int

class AnnualRevenue(BaseModel):
    """年度月度收入统计 (存储过程: proc_statisticsAnnualRevenue)"""
    month: int
    monthlyRevenue: Decimal
    guestCount: int

class GuestCostDetail(BaseModel):
    """退房结算详情 (存储过程: proc_CalculateGuestCost)"""
    guestName: str
    roomNo: str
    roomTypeName: str
    roomPrice: Decimal
    checkInTime: datetime
    checkOutTime: Optional[datetime]
    actualStayDays: int
    depositMoney: Decimal
    roomCost: Decimal
    refundMoney: Decimal
