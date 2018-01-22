# -*- coding: utf-8 -*-
import os,random
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(os.sys.path)
from uuid import uuid4
from sqlalchemy import Column, Integer, String, Text,ForeignKey,Table
from Blog.common.dbhandler import Base,DBHandler
import datetime

class User(Base):
    __tablename__ = 'user'
    random_img=['head1.jpg','head2.jpg','head3.jpg']
    current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = Column(String(40), primary_key=True, default=str(uuid4()))
    name = Column(String(30), nullable=True,unique=True)
    password=Column(String(80),nullable=True)
    email=Column(String(30),nullable=False,unique=True)
    enrolltime = Column(String(30), default=current_time)
    logintime=Column(String(30),default=current_time)
    image = Column(String(30), default='images/%s'%random.choice(random_img))
    islock = Column(Integer, default=0)


if __name__=='__main__':
    DBHandler(Base).init_db()

