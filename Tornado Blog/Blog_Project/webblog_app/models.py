# -*- coding: utf-8 -*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, Text,ForeignKey,Table
from sqlalchemy.orm import relationship
from Blog.common.dbhandler import Base
from Blog.common.dbhandler import DBHandler,DBsession
from Blog.user.usermodel import User
import hashlib
current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Article_Tag(Base):
    __tablename__='article_tag'
    article_id=Column(String(40),ForeignKey('article.id'),primary_key=True)
    tag_id=Column(Integer,ForeignKey('tag.id'),primary_key=True)

class Article(Base):
    __tablename__="article"
    id=Column(String(40),primary_key=True)
    title=Column(String(50),nullable=True,index=True)
    brief = Column(String(300), nullable=True,index=True)
    content = Column(Text, nullable=True)
    date=Column(String(30),default=current_time)
    category_id=Column(Integer,ForeignKey('category.id'))
    category=relationship('Category',backref="article")
    page_views=Column(Integer,default=0)
    image=Column(String(60),nullable=True,default='images/svn.png')
    user_id = Column(String(40), ForeignKey('user.id'))
    user = relationship("User", backref="article")
    article_tag=relationship('Tag', secondary=Article_Tag.__table__)
    
class Category(Base):
    __tablename__="category"
    id=Column(Integer,primary_key=True)
    name=Column(String(10),nullable=True,unique=True)
    urlname=Column(String(20))

class Comment(Base):
    __tablename__="article_comment"
    id = Column(String(40), primary_key=True, default=str(uuid4()))
    content = Column(Text, nullable=True)
    date = Column(String(30), default=current_time)
    article_id=Column(String(40),ForeignKey('article.id'))
    user_id=Column(String(40),ForeignKey('user.id'))
    article=relationship("Article",backref="comment")
    user=relationship("User",backref="comment")

class Tag(Base):
    __tablename__="tag"
    id=Column(Integer,primary_key=True)
    name=Column(String(10),nullable=True,unique=True)
    description = Column(String(200), nullable=True)
    tag_article=relationship('Article', secondary=Article_Tag.__table__)

class Lognote(Base):
    __tablename__="lognote"
    id=Column(Integer,primary_key=True)
    title=Column(String(50),nullable=True)
    brief = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    date=Column(String(30),default=current_time)
    user_id = Column(String(40), ForeignKey('user.id'))
    user = relationship("User", backref="lognote")

class Weblink(Base):
    __tablename__="weblink"
    id=Column(Integer,primary_key=True)
    title=Column(String(50),nullable=True)
    weburl = Column(String(100), nullable=True,unique=True)
    description=Column(String(200),nullable=True)
    date=Column(String(30),default=current_time)
    user_id = Column(String(40), ForeignKey('user.id'))
    user = relationship("User", backref="weblink")

def hash_data(datas):
    h = hashlib.sha1()
    h.update(datas)
    return h.hexdigest()

class UploadFile(Base):
    __tablename__="uploadfile"
    id=Column(Integer,primary_key=True)
    filename=Column(String(50),nullable=True)
    file_type=Column(String(50),nullable=False)
    filesize = Column(Integer, nullable=False)
    _file_hash = Column(String(50), nullable=True, unique=True)
    date=Column(String(30),default=current_time)
    user_id = Column(String(40), ForeignKey('user.id'))
    user = relationship("User", backref="uploadfile")

    @property
    def file_hash(self):
        return self._file_hash

    @file_hash.setter
    def file_hash(self,hashdata):
        self._file_hash=hash_data(hashdata)

if __name__=='__main__':
    DBHandler(Base).init_db()
