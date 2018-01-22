#-*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Blog.settings import DATABASES
from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy import distinct
engine=create_engine("{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset=utf8".format(**DATABASES.get('default')),max_overflow=5)
Base=declarative_base()
DBsession=sessionmaker(bind=engine)()

class DBHandler():
    def __init__(self,Base,column=None,column1=None):
        self.base=Base
        self.column=column
        self.column1=column1
    def init_db(self):
         Base.metadata.create_all(engine)
    def add(self):
        DBsession.add(self.base)
        self.commit()
    def query(self,value=None):
        return DBsession.query(self.base).filter(self.column == value).all()
    def delete(self,value):
        DBsession.query(self.base).filter(self.column == value).delete()
        self.commit()
    def update(self,value,**kwargs):
        DBsession.query(self.base).filter(self.column == value).update(kwargs)
        self.commit()
    def count(self):
        return DBsession.query(func.count(self.column), self.column).group_by(self.column).all()
    def self_count(self,user_id):
        return DBsession.query(func.count(self.column), self.column).filter(self.column1==user_id).group_by(self.column).all()
    def order_desc(self,value=None):
        return DBsession.query(self.base).filter(self.column==value).order_by(self.column1.desc())
    def dist(self):
        return DBsession.query(distinct(self.column)).all()
    def filter_in(self,*args):
        return DBsession.query(self.base).filter(self.column.in_(args)).all()#DBsession.query(Article).filter(Article.id.in_(com_art_list)).all()
    def commit(self):
        DBsession.commit()
if __name__=='__main__':
    DBHandler(Base).init_db()