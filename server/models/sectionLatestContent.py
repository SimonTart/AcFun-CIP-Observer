from sqlalchemy import Column, Integer, String, text, DateTime, func, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class sectionLatestContent(Base):
    __tablename__ = 'section_latest_content'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sectionId = Column('section_id', Integer, nullable=False)
    latestContentDate = Column('latest_content_date', DateTime, nullable=False)
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
