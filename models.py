from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Unicode
from sqlalchemy.orm import relationship
from database import Base
import datetime

class RoomType(Base):
    """
    客房类型模型
    """
    __tablename__ = "roomType"
    __table_args__ = {"implicit_returning": False}

    roomTypeId = Column(String(3), primary_key=True, index=True) # 客房类型编号
    roomTypeName = Column(String(20), nullable=False)           # 客房类型名称
    roomPrice = Column(DECIMAL(10, 2), nullable=False, default=0.00) # 房价
    roomDesc = Column(String(200), nullable=True)                # 客房类型描述

    # 与 RoomInfo 的一对多关系
    rooms = relationship("RoomInfo", back_populates="roomType")

class RoomInfo(Base):
    """
    客房信息模型
    """
    __tablename__ = "roomInfo"
    __table_args__ = {"implicit_returning": False}

    roomNo = Column(String(5), primary_key=True, index=True)    # 房间号
    roomTypeId = Column(String(3), ForeignKey("roomType.roomTypeId"), nullable=False) # 所属客房类型编号
    roomStatus = Column(String(8), nullable=False, default="空闲") # 房间状态 (空闲, 入住, 维修等)
    roomFloor = Column(Integer, nullable=True)                  # 楼层
    roomBedCount = Column(Integer, nullable=True)               # 床位数

    # 与 RoomType 的多对一关系
    roomType = relationship("RoomType", back_populates="rooms")
    # 与 GuestInfo 的一对多关系
    guests = relationship("GuestInfo", back_populates="room")

class GuestInfo(Base):
    """
    宾客入住信息模型
    """
    __tablename__ = "guestInfo"
    __table_args__ = {"implicit_returning": False}

    guestId = Column(Integer, primary_key=True, index=True, autoincrement=True) # 宾客编号
    guestName = Column(Unicode(50), nullable=False)              # 姓名
    guestGender = Column(Unicode(10), nullable=False, default="男") # 性别
    guestAge = Column(Integer, nullable=True)                   # 年龄
    idCard = Column(String(20), nullable=False)                 # 身份证号
    phoneNum = Column(Unicode(20), nullable=True)                # 联系电话
    address = Column(Unicode(200), nullable=True)                # 地址
    workplace = Column(Unicode(100), nullable=True)              # 工作单位
    comeFrom = Column(Unicode(50), nullable=True)                # 籍贯/来源
    checkInTime = Column(DateTime, nullable=False, default=datetime.datetime.now) # 入住时间
    stayDays = Column(Integer, nullable=False)                  # 预计入住天数
    roomNo = Column(String(10), ForeignKey("roomInfo.roomNo"), nullable=True) # 所住房间号
    checkOutTime = Column(DateTime, nullable=True)               # 退房时间
    depositMoney = Column(DECIMAL(10, 2), nullable=False, default=0.00) # 押金
    roomCost = Column(DECIMAL(10, 2), nullable=False, default=0.00)     # 房费累计
    remark = Column(Unicode(200), nullable=True)                 # 备注

    # 与 RoomInfo 的多对一关系
    room = relationship("RoomInfo", back_populates="guests")
