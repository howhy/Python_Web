# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float,DateTime,Boolean
from sqlalchemy.orm import relationship,backref
from utils.dbhandler import Base
from utils.dbhandler import DBHandler
import datetime
from uuid import uuid4

class Device_Type(Base):
    """ 设备"""
    __tablename__ = 'device_type_info'
    device_type_id = Column(String(32),primary_key=True, unique=True)
    device_name =  Column(String(256))
    developer_id = Column(String(32))
    device_key = Column(String(256))
    picture =  Column(String(256))
    model =  Column(String(45))
    control_url = Column(String(256))
    control_version = Column(String(256))
    device_version = Column(String(256))
    device_url = Column(String(256))
    device_url1 = Column(String(256))
    connect_type = Column(Integer,default=0)
    create_time = Column(DateTime,default=datetime.datetime.now)
    update_time = Column(DateTime,default=datetime.datetime.now)
    state = Column(Integer,default=0)
    verify_state = Column(Integer,default=0)
    is_parent_device = Column(Integer,default=0)
    md5 =Column(String(50))
    upgrade_description = Column(String(200))
    language = Column(String(255), default="CN")
    config_url = Column(String(255), default="CN")
    wifi_config = Column(Integer,default=0)


class Device(Base):
    """ 设备信息 """
    __tablename__ = 'device_info'
    device_id = Column(String(32),primary_key=True, unique=True)
    device_type_id = Column(String(32), ForeignKey('device_type_info.device_type_id'))
    device_type = relationship('Device_Type', backref='device')
    #device_name =  Column(String(256))
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    device_key =  Column(String(128))
    state = Column(Integer,default=0)
    unusual = Column(Integer,default=0)


class UserRoom(Base):
    __tablename__ = 'user_room'
    room_id = Column(String(32),primary_key=True, unique=True)
    user_id = Column(String(32), ForeignKey('tab_developer.id'))
    user = relationship('TabDeveloper', backref='user_room')
    room_name = Column(String(45))
    sort_no = Column(Integer,default=0)
    state = Column(Integer,default=0)
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)

class TabDeveloper(Base):
    __tablename__ = 'tab_developer'
    id = Column(String(32),primary_key=True, unique=True)
    account = Column(String(50))
    mobile = Column(String(20))
    nick_name = Column(String(20))
    image_url = Column(String(250))
    app_id = Column(String(32), default="user")
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    state = Column(Integer,default=0)
    unusual = Column(Integer,default=0)
    password = Column(String(50))


class User_Device(Base):
    __tablename__='user_device'
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(32), ForeignKey('tab_developer.id'))
    user = relationship('TabDeveloper', backref='user_device')
    device_id= Column(String(32), ForeignKey('device_info.device_id'))
    device = relationship('Device', backref='user_device_id')
    # parent_device_id = Column(String(32), ForeignKey('device_info.device_id'))
    # parent_device = relationship('Device', backref='user_parent_device')
    # device_type_id = Column(String(32), ForeignKey('device_type_info.device_type_id'))
    # device_type = relationship('Device_Type', backref='user_device')
    device_name = Column(String(45))
    user_name = Column(String(45))
    owner = Column(Integer,default=0)
    user_mobile_phone = Column(String(45))
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    state = Column(Integer,default=0)
    # userroom_id = Column(String(32), ForeignKey('user_room.room_id'))
    # userroom = relationship('UserRoom', backref='user_device')


class SubDeviceInfo(Base):
    """ 子设备 """
    __tablename__ = 'sub_device_info'
    id =  Column(Integer,primary_key=True,autoincrement=True)
    device_id= Column(String(32), ForeignKey('device_info.device_id'))
    device = relationship(Device, backref=backref('sub_device_info'))
    parent_device_id = Column(String(32))#relationship('Device', backref='sub_parent_device')
    #device_type_id = Column(String(32), ForeignKey('device_type_info.device_type_id'))
    #device_type = relationship('Device_Type', backref='sub_device_info')
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    state = Column(Integer,default=0)

class DeviceData(Base):
    """ 设备数据 """
    __tablename__ = 'device_data'
    data_id = Column(String(32),primary_key=True)
    device_type_id = Column(String(32), ForeignKey('device_type_info.device_type_id'))
    device_type = relationship('Device_Type', backref='device_data')
    name = Column(String(32))
    data_format = Column(String(256))
    instruction = Column(String(256))
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    state = Column(Integer,default=0)
    is_public = Column(Boolean,default=1)

class DeviceEvent(Base):
    """ 设备事件 """
    __tablename__ = 'device_event'
    event_id = Column(String(32),primary_key=True)
    device_type_id = Column(String(32), ForeignKey('device_type_info.device_type_id'))
    device_type = relationship('Device_Type', backref='device_event')
    name = Column(String(45))
    value_format = Column(String(256))
    trigger_condition_format = Column(String(256))
    instruction = Column(String(256))
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    state = Column(Integer, default=0)
    is_public = Column(Boolean, default=1)

class DeviceFunction(Base):
    """ 设备方法 """
    __tablename__ = 'device_function'
    function_id = Column(String(32),primary_key=True)
    device_type_id = Column(String(32), ForeignKey('device_type_info.device_type_id'))
    device_type = relationship('Device_Type', backref='device_function')
    name =Column(String(45))
    parameter =Column(String(256))
    instruction = Column(String(256))
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    state = Column(Integer, default=0)
    is_public = Column(Boolean, default=1)
    voice_control = Column(String(256))

class UserFamily(Base):
    __tablename__ = 'tab_my_family'
    id = Column(String(32),primary_key=True, unique=True)
    family_id = Column(String(32))
    user_id = Column(String(32), ForeignKey('tab_developer.id'))
    user = relationship('TabDeveloper', backref='tab_my_family')
    nice_name = Column(String(256))
    is_master = Column(Integer, default=0)
    mobile =Column(String(32))
    update_time = Column(DateTime,default=datetime.datetime.now)
    create_time = Column(DateTime,default=datetime.datetime.now)
    state =  Column(Integer, default=0)
    distinguish_type = Column(Integer, default=1)

if __name__=='__main__':
    #Base.metadata.create_all(engine)
    DBHandler.create_table()