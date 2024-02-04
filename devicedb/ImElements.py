#-*- coding:UTF-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from devicedb.Imbase import engine

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


class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_type = Column(String(32), unique=True)
    device_code = Column(String(32), unique=True)
    device_name = Column(String(32), nullable=True, index=True)
    device_contact = Column(String(32), unique=True)
    device_msg = Column(String(32), unique=True)
    host = Column(String(32), unique=True)
    port = Column(String(32), unique=True)


Base.metadata.create_all(engine)  # 这是将所有类都进行转换为表的语句
