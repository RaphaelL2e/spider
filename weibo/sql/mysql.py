from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker

# 创建对象的基类:
Base = declarative_base()


class HotTop(Base):
    __tablename__ = 'hot_top'

    id = Column(Integer, primary_key=True, autoincrement=True)
    issue = Column(String(12))
    ranking = Column(Integer)
    heat = Column(Integer)
    title = Column(String(255))
    url = Column(String(255))


engine = create_engine('mysql://root:leeyfMysql100%@106.15.198.212:3306/weibo_data')


def insert_hot_top(data:[]):
    session = Session(engine)
    session.add_all(data)
    session.flush()
    session.commit()
    session.close_all()

