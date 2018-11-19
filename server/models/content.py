from sqlalchemy import Column, Integer, String, text, DateTime, func, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True, autoincrement=False)
    type = Column(String(255))
    contentType = Column('content_type', String(255), nullable=False)
    channelId = Column('channel_id', Integer)
    realmId = Column('realm_id', Integer)
    realmName = Column('realm_name', String(255))
    latestCommentTime = Column('latest_comment_time', String(255))
    title = Column(String(255), nullable=False)
    viewNum = Column('view_num', Integer, nullable=False)
    commentNum = Column('comment_num', Integer, nullable=False)
    bananaNum = Column('banana_num', Integer)
    publishedAt = Column('published_at', DateTime, nullable=False)
    publishedBy = Column('published_by', Integer, nullable=False)
    isGetComments = Column('is_get_comments', Boolean, server_default=text('FALSE'))
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
