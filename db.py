import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import db

connect_url = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(**db);
engine = create_engine(connect_url, encoding='utf8')

Session = sessionmaker(bind=engine)
connection = engine.connect()
