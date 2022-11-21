#-*- coding:UTF-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from db.base import engine

Base = declarative_base()  # 所有的类都要继承自这个基础类

# 元素表
class Devices(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    devicesId = Column(String(32), unique=True)
    alarm = Column(String(32), nullable=True, index=True)
    fault = Column(String(32), unique=True)
    common = Column(String(32), unique=True)
    status = Column(String(32), unique=True)
    isAlert = Column(String(32), unique=True)
    devicesStatusLink = Column(String(32), unique=True)
    conProfix = Column(String(32), unique=True)
    conPort = Column(String(32), unique=True)
    configId = Column(String(32), unique=True)
    searchTimeField = Column(String(32), unique=True)
    checkTime = Column(String(32), unique=True)


# 配置表
class Config(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(32), nullable=False)
    pwd = Column(String(32), nullable=False)
    platformPrefix = Column(String(32), nullable=False)
    platformPort = Column(String(32), nullable=False)
    platformType = Column(String(32), nullable=False)
    status = Column(String(32), nullable=False)

class DevicesLog(Base):
    __tablename__ = "devices_time"
    id = Column(Integer, primary_key=True, autoincrement=True)
    devicesId = Column(String(32), nullable=False)
    logTime = Column(String(32), nullable=False)
    executeLog = Column(String(32), nullable=False)
    result = Column(String(32), nullable=False)
    describe = Column(String(32), nullable=False)

Base.metadata.create_all(engine)  # 这是将所有类都进行转换为表的语句
