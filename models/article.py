from sqlalchemy import Column, Integer, String, DateTime, func
from . import base


class Article(base.Base):
  __tablename__ = 'articles'
  id = Column(Integer, primary_key = True)
  type = Column(String(255), nullable = False)
  title = Column(String(255), nullable = False)
  viewNum = Column('view_num', Integer, nullable = True)
  commentNum = Column('comment_num', Integer, nullable = True)
  publishedAt = Column('published_at', DateTime, nullable = True)
  publishedBy = Column('published_by', Integer, nullable = True)
  # updateAt = Column('updated_at', server_onupdate = func.utc_timestamp())
  # createAt = Column('created_at', DateTime, server_default = func.utc_timestamp())

