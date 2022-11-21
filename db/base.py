from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,Index
from sqlalchemy.orm import sessionmaker,relationship
import pymysql
# host = 10.0.0.143
# ;database = api_testing
# database = rabbit-v2
# username = root
# passwrod = 123456
engine = create_engine("mysql+pymysql://root:123456@10.0.0.143:3306/device_send_info?charset=utf8",
                       echo=True,
                       pool_size=8,
                       pool_recycle=60*30
                       )
