from sqlalchemy import Column, Integer, String, DateTime, func
from . import base

class User(base.Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key = True)

        