from sqlalchemy import Column, Integer, String, text, DateTime, func, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SpiderRecord(Base):
    __tablename__ = 'spider_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    channelId = Column('channel_id', Integer)
    type = Column(String(255), nullable=False)
    successDate = Column('success_date', DateTime, nullable=False)
    updateAt = Column(
        'updated_at',
        DateTime,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )
    createAt = Column(
        'created_at',
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )
