# 导入:
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name

# 初始化数据库连接:
engine = create_engine('postgresql+psycopg2://postgres:root@127.0.0.1:5432/postgres')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)