#-*- coding:utf-8 -*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASES
from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy import distinct
Base=declarative_base()

class DBHandler():
    __singleobj=None
    __engine = create_engine("{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset=utf8".format(**DATABASES.get('default')),max_overflow=5, pool_recycle=3600)
    def __init__(self,base=Base):
        self.base=base
    @classmethod
    def session(cls):
        if not cls.__singleobj:
            cls.__singleobj=sessionmaker(bind=cls.__engine)()
        return cls.__singleobj
    @classmethod
    def create_table(cls):
        Base.metadata.create_all(cls.__engine)

    def dbsession(self):
        return DBHandler.session()

    def query(self,**kwargs):
        return self.dbsession().query(self.base).filter_by(**kwargs)

    def add(self):
        self.dbsession().add(self.base)
        self.commit()


DBsession = DBHandler.session()
