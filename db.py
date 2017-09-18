import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

if os.getenv('PYTHON_ENV', 'development') == 'production':
  user = os.getenv('DB_USER')
  password = os.getenv('DB_PASSWORD')
  engine = create_engine('mysql+pymysql://{user}:{password}@127.0.0.1/eva_acfun?charset=utf8'.format(user=user,password=password), encoding='utf8')
else:
  engine = create_engine('mysql+pymysql://root@127.0.0.1/eva_acfun_test?charset=utf8', encoding='utf8', echo = False)

models.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
