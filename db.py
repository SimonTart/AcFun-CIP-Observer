import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

# if os.environ['PYTHON_ENV'] == 'dev':
engine = create_engine('mysql+pymysql://root@127.0.0.1/eva_acfun_test?charset=utf8', encoding='utf8', echo = True)

models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

# def session:
#   return Session()
