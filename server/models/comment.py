from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comment(Base):
  __tablename__ = 'comments'
  id = Column(Integer, primary_key = True, autoincrement = False)
  content = Column(Text)
  userId = Column('user_id', Integer)
  postDate = Column('post_date', DateTime)
  quoteId = Column(Integer)
  isDelete = Column('is_delete', Boolean, nullable=False)
  isUpDelete = Column('is_up_delete', Boolean, nullable=False)
  contentId = Column('content_id', Integer, nullable=False)
  updateAt = Column(
    'updated_at',
    DateTime,
    nullable=False,
    server_default = text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
  )
  createAt = Column(
    'created_at',
    DateTime,
    nullable=False,
    server_default = func.current_timestamp()
  )
