import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

if os.environ['PYTHON_ENV'] == 'production':
  engine = create_engine(f'mysql+pymysql://${os.environ['DB_USER']}:{os.environ['DB_PASSPORT']}@127.0.0.1/eva_acfun?charset=utf8', encoding='utf8')
else
  engine = create_engine('mysql+pymysql://root@127.0.0.1/eva_acfun_test?charset=utf8', encoding='utf8', echo = True)

models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
