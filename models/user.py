from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column('id', Integer, primary_key = True, autoincrement = False)
  name = Column('name', String(255))
  sign = Column('sign', Text)
  avatar = Column('avatar', String(255))
  postNum = Column('post_num', Integer, doc='投稿数')
  postArticleNum = Column('post_article_num', Integer, doc='投稿的文章数')
  postVideoNum = Column('post_video_num', Integer, doc='投稿的视频数')
  comeFrom = Column('come_from', String(255))
  lastLoginIp = Column('last_login_ip', String(255))
  exp = Column('exp', Integer)
  fansNum = Column('fans_num', Integer)
  followNum = Column('follow_num', Integer)
  gender = Column('gender', Boolean)
  registerAt = Column('register_at', DateTime)
  disabled = Column('disabled', Boolean, server_default=text('FALSE'))
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
  