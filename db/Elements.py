# -*- coding:UTF-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from db.base import engine

Base = declarative_base()  # 所有的类都要继承自这个基础类


# 设备信息
class Device_info(Base):
    __tablename__ = "device_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_type = Column(String(32), unique=True)
    device_prefix = Column(String(32), unique=True)
    device_alarm = Column(String(32), nullable=True, index=True)
    device_fault = Column(String(32), unique=True)
    device_alarm_restore = Column(String(32), unique=True)
    device_fault_restore = Column(String(32), unique=True)
    remark = Column(String(32), unique=True)


# 元素表
class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(32), unique=True)
    host = Column(String(32), unique=True)
    port = Column(String(32), unique=True)
    p_id = Column(String(11), nullable=True)
    type = Column(String(11), nullable=True)
    device_type = Column(String(11), nullable=True)


# 配置表
class Config(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(32), nullable=False)
    pwd = Column(String(32), nullable=False)
    platformPrefix = Column(String(32), nullable=False)
    status = Column(String(32), nullable=False)
    device_type = Column(String(11), nullable=True)
    page_size = Column(String(11), nullable=True)



Base.metadata.create_all(engine)  # 这是将所有类都进行转换为表的语句
