#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import json
import copy
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from utils.redisdb import handler as redisdb
from utils import mongodb_client
from utils.strTools import get_uuid
from utils.exceptions import NoDataInDB
from utils import user_notice_msg
from django.db.models import Q
import traceback

def save(obj, force_insert=False, force_update=False, using=None,
         update_fields=None):
    for field in obj._meta.get_fields():
        if isinstance(field, models.CharField):
            attribute = getattr(obj, field.name)
            if attribute == None:
                attribute = ""
            if len(attribute) > field.max_length:
                raise MaxLengthError("{} is to long".format(field.name))
    obj.mysave(force_insert=force_insert, force_update=force_update, using=using,
               update_fields=update_fields)

models.Model.mysave = models.Model.save

models.Model.save = save


def qiniu_url_format(name):
    if name is not None:
        return settings.QI_NIU_URL + name
    return ""


class MaxLengthError(Exception):
    pass


class DeviceType(models.Model):
    """ 设备类型 """
    device_type_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_name = models.CharField(max_length=256)
    developer_id = models.CharField(max_length=32)
    device_key = models.CharField(max_length=256)
    picture_name = models.CharField(max_length=256, db_column='picture')
    model = models.CharField(max_length=45)
    control_url_name = models.CharField(
        max_length=256, db_column='control_url')
    control_version = models.CharField(max_length=256)
    device_version = models.CharField(max_length=256)
    device_url_name = models.CharField(max_length=256, db_column="device_url")
    device_url1_name = models.CharField(
        max_length=256, db_column="device_url1")
    connect_type = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=0)
    verify_state = models.IntegerField(default=0)
    is_parent_device = models.IntegerField(default=0)
    md5 = models.CharField(max_length=50)
    upgrade_description = models.CharField(max_length=200)
    language = models.CharField(max_length=255, default="CN")
    config_url_name = models.CharField(max_length=255, db_column='config_url')
    """device_type_info 表 加 wifi_config 字段 默认为0 ， 0:smart_config 1:smart_config+ap 2:ap 3:air_kiss"""
    wifi_config = models.IntegerField(default=0)

    class Meta:
        db_table = "device_type_info"

    @property
    def picture(self):
        return qiniu_url_format(self.picture_name)

    @property
    def control_url(self):
        return qiniu_url_format(self.control_url_name)

    @property
    def device_url(self):
        if self.device_url_name is not None and not "" == self.device_url_name:
            return settings.QI_NIU_URL1 + self.device_url_name
        return ""

    @property
    def device_url1(self):
        if self.device_url1_name is not None and not "" == self.device_url1_name:
            return settings.QI_NIU_URL1 + self.device_url1_name
        return ""

    @property
    def config_url(self):
        if self.config_url_name:
            return qiniu_url_format(self.config_url_name)
        return ""

class DeviceTypeDE(models.Model):
    """ 设备类型 """
    device_type_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_name = models.CharField(max_length=256)
    developer_id = models.CharField(max_length=32)
    device_key = models.CharField(max_length=256)
    picture_name = models.CharField(max_length=256, db_column='picture')
    model = models.CharField(max_length=45)
    control_url_name = models.CharField(
        max_length=256, db_column='control_url')
    control_version = models.CharField(max_length=256)
    device_version = models.CharField(max_length=256)
    device_url_name = models.CharField(max_length=256, db_column="device_url")
    device_url1_name = models.CharField(
        max_length=256, db_column="device_url1")
    connect_type = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=0)
    verify_state = models.IntegerField(default=0)
    is_parent_device = models.IntegerField(default=0)
    md5 = models.CharField(max_length=50)
    upgrade_description = models.CharField(max_length=200)
    language = models.CharField(max_length=255, default="CN")
    config_url_name = models.CharField(max_length=255, db_column='config_url')
    wifi_config = models.IntegerField(default=0)

    class Meta:
        db_table = "device_type_info_de"

    @property
    def picture(self):
        return qiniu_url_format(self.picture_name)

    @property
    def control_url(self):
        return qiniu_url_format(self.control_url_name)

    @property
    def device_url(self):
        if self.device_url_name is not None and not "" == self.device_url_name:
            return settings.QI_NIU_URL1 + self.device_url_name
        return ""

    @property
    def device_url1(self):
        if self.device_url1_name is not None and not "" == self.device_url1_name:
            return settings.QI_NIU_URL1 + self.device_url1_name
        return ""

    @property
    def config_url(self):
        if self.config_url_name:
            return qiniu_url_format(self.config_url_name)
        return ""

class DeviceTypeEN(models.Model):
    """ 设备类型 """
    device_type_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_name = models.CharField(max_length=256)
    developer_id = models.CharField(max_length=32)
    device_key = models.CharField(max_length=256)
    picture_name = models.CharField(max_length=256, db_column='picture')
    model = models.CharField(max_length=45)
    control_url_name = models.CharField(
        max_length=256, db_column='control_url')
    control_version = models.CharField(max_length=256)
    device_version = models.CharField(max_length=256)
    device_url_name = models.CharField(max_length=256, db_column="device_url")
    device_url1_name = models.CharField(
        max_length=256, db_column="device_url1")
    connect_type = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=0)
    verify_state = models.IntegerField(default=0)
    is_parent_device = models.IntegerField(default=0)
    md5 = models.CharField(max_length=50)
    upgrade_description = models.CharField(max_length=200)
    language = models.CharField(max_length=255, default="CN")
    config_url_name = models.CharField(max_length=255, db_column='config_url')
    wifi_config = models.IntegerField(default=0)

    class Meta:
        db_table = "device_type_info_en"

    @property
    def picture(self):
        return qiniu_url_format(self.picture_name)

    @property
    def control_url(self):
        return qiniu_url_format(self.control_url_name)

    @property
    def device_url(self):
        if self.device_url_name is not None and not "" == self.device_url_name:
            return settings.QI_NIU_URL1 + self.device_url_name
        return ""

    @property
    def device_url1(self):
        if self.device_url1_name is not None and not "" == self.device_url1_name:
            return settings.QI_NIU_URL1 + self.device_url1_name
        return ""

    @property
    def config_url(self):
        if self.config_url_name:
            return qiniu_url_format(self.config_url_name)
        return ""

class DeviceTypeFR(models.Model):
    """ 设备类型 """
    device_type_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_name = models.CharField(max_length=256)
    developer_id = models.CharField(max_length=32)
    device_key = models.CharField(max_length=256)
    picture_name = models.CharField(max_length=256, db_column='picture')
    model = models.CharField(max_length=45)
    control_url_name = models.CharField(
        max_length=256, db_column='control_url')
    control_version = models.CharField(max_length=256)
    device_version = models.CharField(max_length=256)
    device_url_name = models.CharField(max_length=256, db_column="device_url")
    device_url1_name = models.CharField(
        max_length=256, db_column="device_url1")
    connect_type = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=0)
    verify_state = models.IntegerField(default=0)
    is_parent_device = models.IntegerField(default=0)
    md5 = models.CharField(max_length=50)
    upgrade_description = models.CharField(max_length=200)
    language = models.CharField(max_length=255, default="CN")
    config_url_name = models.CharField(max_length=255, db_column='config_url')
    wifi_config = models.IntegerField(default=0)

    class Meta:
        db_table = "device_type_info_fr"

    @property
    def picture(self):
        return qiniu_url_format(self.picture_name)

    @property
    def control_url(self):
        return qiniu_url_format(self.control_url_name)

    @property
    def device_url(self):
        if self.device_url_name is not None and not "" == self.device_url_name:
            return settings.QI_NIU_URL1 + self.device_url_name
        return ""

    @property
    def device_url1(self):
        if self.device_url1_name is not None and not "" == self.device_url1_name:
            return settings.QI_NIU_URL1 + self.device_url1_name
        return ""

    @property
    def config_url(self):
        if self.config_url_name:
            return qiniu_url_format(self.config_url_name)
        return ""

class Device(models.Model):
    """ 设备信息 """
    device_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey(
        "DeviceType", related_name="devices", to_field='device_type_id')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    device_key = models.CharField(max_length=128)
    state = models.IntegerField(default=0)
    unusual = models.IntegerField(default=0)

    class Meta:
        db_table = "device_info"

    def delete_sub_device(self, sub_id=None):
        """ 删除子设备 """
        query = Q(state=1, parent_device_id=self.device_id)
        if sub_id is not None:
            query = query & Q(device_id=sub_id)
        SubDeviceInfo.objects.filter(query).delete()
        return True

class SubDeviceInfo(models.Model):
    """ 子设备 """
    id = models.IntegerField(primary_key=True)
    device = models.ForeignKey(
        "Device", to_field='device_id')
    parent_device = models.ForeignKey(
        "Device", to_field='device_id', related_name='sub_devices')
    device_type = models.ForeignKey(
        "DeviceType", related_name="sub_device_type", to_field='device_type_id')
    device_name = models.CharField(max_length=45)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)

    class Meta:
        db_table = "sub_device_info"
        unique_together = ("device", "parent_device")


class User_Device(models.Model):
    """ 用户设备关联表 """
    user_id = models.CharField(max_length=32)
    device = models.ForeignKey("Device", to_field='device_id')
    device_type = models.ForeignKey("DeviceType", to_field='device_type_id')
    owner = models.IntegerField(default=0)
    device_name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    # 2017.08.02 字段扩展
    room = models.ForeignKey("UserRoom", to_field="room_id")
    # room_id = models.CharField(max_length=45)
    parent_device = models.ForeignKey("Device", to_field="device_id")
    user_mobile_phone = models.CharField(max_length=45)

    class Meta:
        db_table = "user_device"
        unique_together = (("user_id", "device", "parent_device_id"),)

    @property
    def user(self):
        user = None
        try:
            user = TabDeveloper.objects.get(id=self.user_id)
        except TabDeveloper.DoesNotExist:
            user = TabDeveloper(
                id=self.user_id,
                nick_name="",
                image_url="",
                mobile="",
            )
        return user

class DeviceData(models.Model):
    """ 设备数据 """
    data_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceType", to_field='device_type_id')
    name = models.CharField(max_length=45)
    data_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_data"

class DeviceDataDE(models.Model):
    """ 设备数据 """
    data_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeDE", to_field='device_type_id')
    name = models.CharField(max_length=45)
    data_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_data_de"

class DeviceDataEN(models.Model):
    """ 设备数据 """
    data_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeEN", to_field='device_type_id')
    name = models.CharField(max_length=45)
    data_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_data_en"

class DeviceDataFR(models.Model):
    """ 设备数据 """
    data_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeFR", to_field='device_type_id')
    name = models.CharField(max_length=45)
    data_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_data_fr"

class DeviceEvent(models.Model):
    """ 设备事件 """
    event_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceType", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    trigger_condition_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_event"

    def __unicode__(self):
        return self.name

    @classmethod
    def get_device(cls, id):
            # 如果没有该设备则查看子设备中是否有该设备
            device_id = str(id)
            try:
                return Device.objects.get(device_id=device_id)
            except:
                devices = SubDeviceInfo.objects.filter(device_id=device_id)
                if devices:
                    return devices[0]
                else:   # 没有该设备
                    raise NoDataInDB("Device does not exist!", [device_id])

    @classmethod
    def save_execute_log(cls, data):
        """ 保存日志 """
        devicelogdb = mongodb_client.mongodb(
            settings.MONGODB_DB_DEVICE_LOG, settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)
        log_id = data.get("device_id", data["from_id"])
        event_log_name = "event_log_{}".format(log_id)
        event_log_value = {
            "event_id": data["event_id"],
            "event_name": data["event_name"],
            "event_value": data.get("event_value", []),
            "time": datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S") if data.get("time","") else datetime.now()
        }
        # event_resp_value = copy.deepcopy(event_log_value)
        # event_resp_value["time"] = event_resp_value["time"].strftime("%Y-%m-%d %H:%M:%S")

        # datetime类型不能被jsonfy
        event_log_value["time"] = event_log_value["time"].strftime("%Y-%m-%d %H:%M:%S")

        devicelogdb.insertcollect(event_log_name, event_log_value)
        del event_log_value["_id"]
        return event_log_value


    @classmethod
    def save_execute_smart_control_log(cls, smart_control):
        db = mongodb_client.mongodb(settings.MONGODB_DB_SMART_CONTROL_LOG,
                                    settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)

        query = Q(state=1, event_id=smart_control.event_id)  # 存在空情况

        if smart_control.device_id:
            device = DeviceEvent.get_device(smart_control.device_id)
            device_type_id = device.device_type_id
            query = query & Q(device_type_id=device_type_id)

        events = DeviceEvent.objects.filter(query)
        if events.count() > 0:
            event = events[0]
            values = {
                "user_id": smart_control.user_id,
                "smart_id": smart_control.smart_id,
                "smart_name": smart_control.name,
                "event_name": event.name,
                "log_info": "场景被触发",
                "time": datetime.now()
            }
            db.insertcollect("execute_smart_control_log", values)
            return values
        return dict()

class DeviceEventDE(models.Model):
    """ 设备事件 """
    event_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeDE", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    trigger_condition_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_event_de"

    def __unicode__(self):
        return self.name

    @classmethod
    def save_execute_log(cls, data):
        """ 保存日志 """
        devicelogdb = mongodb_client.mongodb(
            settings.MONGODB_DB_DEVICE_LOG, settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)
        log_id = data.get("device_id", data["from_id"])
        event_log_name = "event_log_{}".format(log_id)
        event_log_value = {
            "event_id": data["event_id"],
            "event_name": data["event_name"],
            "event_value": data.get("event_value", []),
            "time": datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S") if data.get("time","") else datetime.now()
        }
        event_log_value["time"] = event_log_value["time"].strftime("%Y-%m-%d %H:%M:%S")

        devicelogdb.insertcollect(event_log_name, event_log_value)
        del event_log_value["_id"]
        return event_log_value

    @classmethod
    def save_execute_smart_control_log(cls, smart_control):
        db = mongodb_client.mongodb(settings.MONGODB_DB_SMART_CONTROL_LOG,
                                    settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)

        query = Q(state=1, event_id=smart_control.event_id)
        if smart_control.device_id:
            device = DeviceEvent.get_device(smart_control.device_id)
            device_type_id = device.device_type_id
            query = query & Q(device_type_id=device_type_id)
        events = DeviceEventDE.objects.filter(query)
        if events.count() > 0:
            event = events[0]
            values = {
                "user_id": smart_control.user_id,
                "smart_id": smart_control.smart_id,
                "smart_name": smart_control.name,
                "event_name": event.name,
                "log_info": "场景被触发",
                "time": datetime.now()
            }
            db.insertcollect("execute_smart_control_log", values)
            return values
        return dict()

class DeviceEventEN(models.Model):
    """ 设备事件 """
    event_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeEN", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    trigger_condition_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_event_en"

    def __unicode__(self):
        return self.name

    @classmethod
    def save_execute_log(cls, data):
        """ 保存日志 """
        devicelogdb = mongodb_client.mongodb(
            settings.MONGODB_DB_DEVICE_LOG, settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)
        log_id = data.get("device_id", data["from_id"])
        event_log_name = "event_log_{}".format(log_id)
        event_log_value = {
            "event_id": data["event_id"],
            "event_name": data["event_name"],
            "event_value": data.get("event_value", []),
            "time": datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S") if data.get("time") else datetime.now()
        }
        event_log_value["time"] = event_log_value["time"].strftime("%Y-%m-%d %H:%M:%S")

        devicelogdb.insertcollect(event_log_name, event_log_value)
        del event_log_value["_id"]
        return event_log_value

    @classmethod
    def save_execute_smart_control_log(cls, smart_control):
        db = mongodb_client.mongodb(settings.MONGODB_DB_SMART_CONTROL_LOG,
                                    settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)

        query = Q(state=1, event_id=smart_control.event_id)
        if smart_control.device_id:
            device = DeviceEvent.get_device(smart_control.device_id)
            device_type_id = device.device_type_id
            query = query & Q(device_type_id=device_type_id)
        events = DeviceEventEN.objects.filter(query)
        if events.count() > 0:
            event = events[0]
            values = {
                "user_id": smart_control.user_id,
                "smart_id": smart_control.smart_id,
                "smart_name": smart_control.name,
                "event_name": event.name,
                "log_info": "场景被触发",
                "time": datetime.now()
            }
            db.insertcollect("execute_smart_control_log", values)
            return values
        return dict()

class DeviceEventFR(models.Model):
    """ 设备事件 """
    event_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeFR", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    trigger_condition_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)

    class Meta:
        db_table = "device_event_fr"

    def __unicode__(self):
        return self.name

    @classmethod
    def save_execute_log(cls, data):
        """ 保存日志 """
        devicelogdb = mongodb_client.mongodb(
            settings.MONGODB_DB_DEVICE_LOG, settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)
        log_id = data.get("device_id", data["from_id"])
        event_log_name = "event_log_{}".format(log_id)
        event_log_value = {
            "event_id": data["event_id"],
            "event_name": data["event_name"],
            "event_value": data.get("event_value", []),
            "time": datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S") if data.get("time","") else datetime.now()
        }
        event_log_value["time"] = event_log_value["time"].strftime("%Y-%m-%d %H:%M:%S")

        devicelogdb.insertcollect(event_log_name, event_log_value)
        del event_log_value["_id"]
        return event_log_value

    @classmethod
    def save_execute_smart_control_log(cls, smart_control):
        db = mongodb_client.mongodb(settings.MONGODB_DB_SMART_CONTROL_LOG,
                                    settings.MONGODB_HOST_PUBLIC, settings.MONGODB_PORT_PUBLIC, settings.MONGODB_NAME, settings.MONGODB_PASS)

        query = Q(state=1, event_id=smart_control.event_id)
        if smart_control.device_id:
            device = DeviceEvent.get_device(smart_control.device_id)
            device_type_id = device.device_type_id
            query = query & Q(device_type_id=device_type_id)
        events = DeviceEventFR.objects.filter(query)
        if events.count() > 0:
            event = events[0]
            values = {
                "user_id": smart_control.user_id,
                "smart_id": smart_control.smart_id,
                "smart_name": smart_control.name,
                "event_name": event.name,
                "log_info": "场景被触发",
                "time": datetime.now()
            }
            db.insertcollect("execute_smart_control_log", values)
            return values
        return dict()

class DeviceFunction(models.Model):
    """ 设备方法 """
    function_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceType", to_field='device_type_id')
    name = models.CharField(max_length=45)
    parameter = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)


    class Meta:
        db_table = "device_function"

class DeviceFunctionDE(models.Model):
    """ 设备方法 """
    function_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeDE", to_field='device_type_id')
    name = models.CharField(max_length=45)
    parameter = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)

    class Meta:
        db_table = "device_function_de"

class DeviceFunctionEN(models.Model):
    """ 设备方法 """
    function_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeEN", to_field='device_type_id')
    name = models.CharField(max_length=45)
    parameter = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)

    class Meta:
        db_table = "device_function_en"

class DeviceFunctionFR(models.Model):
    """ 设备方法 """
    function_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeFR", to_field='device_type_id')
    name = models.CharField(max_length=45)
    parameter = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)

    class Meta:
        db_table = "device_function_fr"

class DeviceStatus(models.Model):
    status_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceType", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)

    def set_value_format(self, vf):
        self.value_format = json.dumps(vf)

    def get_value_format(self):
        return json.loads(self.value_format)

    class Meta:
        db_table = "device_status"

    @classmethod
    def opera(cls, condition_list, device_status_list):
        '''
        比较满足的条件
        status:{"name":xxx,"value":xxx}
        condition:{"parameter_name":xxx, "comparison_value":xxx}
        '''
        OPERATORS = {
            "=": lambda a, b: a == b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            "!=": lambda a, b: a != b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b
        }

        def _is_satisfy_condition_exited(condition): #是否存在满足条件的状态
            for device_status in device_status_list:
                func = OPERATORS.get(condition["comparison_operator"], "=")
                name1 = condition["parameter_name"]
                name2 = device_status["name"]
                if name1 != name2:
                    continue
                if condition["comparison_operator"] == "=":
                    if '\u5f00' == device_status["value"]: device_status["value"] = '1'  # 开
                    if '\u5173' == device_status["value"]: device_status["value"] = '0'  # 关
                    result2 = func(device_status["value"], condition["comparison_value"])
                else:
                    result2 = func(float(device_status["value"]), float(condition["comparison_value"]))
                if result2:
                    return True
            return False
        ret = map(_is_satisfy_condition_exited, condition_list)  # [True, False]
        return ret






    # def opera(cls, exc, value):
    #     if exc[""] == "=":
    #         return cmp(exc["comparison_value"], value) == 0
    #     if exc[""] == ">":
    #         return value > exc["comparison_value"]
    #     if exc[""] == "<":
    #         return value < exc["comparison_value"]
    #     return False

class DeviceStatusDE(models.Model):
    status_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeDE", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)

    def set_value_format(self, vf):
        self.value_format = json.dumps(vf)

    def get_value_format(self):
        return json.loads(self.value_format)

    class Meta:
        db_table = "device_status_de"

    @classmethod
    def opera(cls, exc, value):
        return DeviceStatus.opera(exc, value)
        # if exc[""] == "=":
        #     return cmp(exc["comparison_value"], value) == 0
        # if exc[""] == ">":
        #     return value > exc["comparison_value"]
        # if exc[""] == "<":
        #     return value < exc["comparison_value"]
        # return False

class DeviceStatusEN(models.Model):
    status_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeEN", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)

    def set_value_format(self, vf):
        self.value_format = json.dumps(vf)

    def get_value_format(self):
        return json.loads(self.value_format)

    class Meta:
        db_table = "device_status_en"

    @classmethod
    def opera(cls, exc, value):
        return DeviceStatus.opera(exc, value)
        # if exc[""] == "=":
        #     return cmp(exc["comparison_value"], value) == 0
        # if exc[""] == ">":
        #     return value > exc["comparison_value"]
        # if exc[""] == "<":
        #     return value < exc["comparison_value"]
        # return False

class DeviceStatusFR(models.Model):
    status_id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type = models.ForeignKey("DeviceTypeFR", to_field='device_type_id')
    name = models.CharField(max_length=45)
    value_format = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    is_public = models.BooleanField(default=1)
    voice_control = models.CharField(max_length=256)

    def set_value_format(self, vf):
        self.value_format = json.dumps(vf)

    def get_value_format(self):
        return json.loads(self.value_format)

    class Meta:
        db_table = "device_status_fr"

    @classmethod
    def opera(cls, exc, value):
        return DeviceStatus.opera(exc, value)
        # if exc[""] == "=":
        #     return cmp(exc["comparison_value"], value) == 0
        # if exc[""] == ">":
        #     return value > exc["comparison_value"]
        # if exc[""] == "<":
        #     return value < exc["comparison_value"]
        # return False

class EventTrigger(models.Model):
    trigger_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    trigger_type = models.IntegerField(default=1, null=False, blank=False)
    event = models.ForeignKey("DeviceEvent", to_field='event_id')
    device = models.ForeignKey(
        "Device", to_field='device_id', related_name='device_event_trigger')
    parent_device = models.ForeignKey(
        "Device", to_field='device_id', related_name='parent_device_event_trigger')
    trigger_condition = models.CharField(max_length=1000)
    name = models.CharField(max_length=45)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)

    class Meta:
        db_table = "event_trigger"


class Manufacturer(models.Model):
    manufacturer_id = models.CharField(
        primary_key=True, unique=True, max_length=32)
    name = models.CharField(max_length=45)
    user_type = models.IntegerField(default=0)
    mobile = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)

    class Meta:
        db_table = "manufacturer_info"


class SmartControl(models.Model):
    smart_id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=256)
    user_id = models.CharField(max_length=256)
    # event = models.ForeignKey("DeviceEvent", to_field="event_id")
    event_id = models.CharField(max_length=32)
    device = models.ForeignKey("Device", to_field="device_id")
    parent_device_id = models.CharField(max_length=256)
    instruction = models.CharField(max_length=256)
    condition_info = models.TextField()
    control_info = models.TextField()
    action_type = models.IntegerField(default=1)
    smart_type = models.CharField(max_length=256, default="0")
    switch = models.IntegerField(default=0)
    condition_type = models.IntegerField(default=2)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)

    class Meta:
        db_table = "smart_control"

    @property
    def event(self):
        '''
        if mysql has this event_id return the querySet
        else return a event which is first step event in condition_info dict
        '''
        events = DeviceEvent.objects.filter(event_id=self.event_id)
        if events.count() > 0:
            return events[0]

        event_name = [item["event_name"] for item in self.condition_info if item["step"] == "1"]
        event_type = [item["type"] for item in self.condition_info if item["step"] == "1"]

        return DeviceEvent(
                device_type_id = event_type,
                event_id=self.event_id,
                name=event_name[0],
                state=1
            )

    def add_timer(self):
        '''
        set timer info
        return to cloudring/server/timer/1.0/
        '''
        reqInfo = []
        condition_info = json.loads(self.condition_info)
        step1 = [item for item in condition_info if item["step"] == "1"][0]

        if step1["type"] == "timer":
            timer = step1
            action_time = timer['time']
            now = datetime.now()
            action_time = datetime.strptime("{}-{}-{} {}".format(now.year, now.month, now.day, action_time),
                                            "%Y-%m-%d %H:%M:%S")
            if action_time <= now:
                action_time = action_time + timedelta(days=1)
            action_time = action_time.strftime("%Y-%m-%d %H:%M:%S")

            action_info = {
                "from_type": "user",
                "from_id": self.user_id,
                "to_type": settings.EVENT_SERVER_TOPIC[0][10:-1],  # "server_event",
                "to_id": "",
                "cmd": "device_event",
                "event_id": self.event_id,
                "event_name": timer["event_name"],
                "user_id": self.user_id
            }

            add_timer_data = {
                # "from_type": "server/event/1.0/",
                "from_type": settings.EVENT_SERVER_TOPIC[0][10:-1],  # server/event/1.0/  去除斜杠
                "from_id": "",
                "to_type": "server_timer",
                "to_id": "",
                "cmd": "add_timer",
                "user_id": self.user_id,
                "timer_id": get_uuid(),
                "timer_name": self.name,
                "action_name": "",
                "action_time": action_time,
                "cycle_type": timer["cycle_type"],
                "cycle_parameter": timer["cycle_parameter"],
                "action_info": json.dumps(action_info)
            }
            # reqInfo.append(("cloudring/server/timer/1.0/", add_timer_data))
            reqInfo.append((settings.TIMER_SERVER_TOPIC[0], add_timer_data))
        return reqInfo

    def execute(self, to_log=None, data=None, client=None):
        '''
        step1.type:
            timer, hand_click --> do_work
            event --> return list for condition_info[type=="status"] to cloudring/device
        '''
        reqInfo = []
        condition_info = json.loads(self.condition_info)
        # step1为事件，其余为条件（如“门磁关灯光暗”的时候开灯，“门磁关”是触发事件上报的事件，“灯光暗”是执行该场景的条件）
        step1 = [item for item in condition_info if item["step"] == "1"][0]

        if len(condition_info) == 1:
            if step1["type"] in ["timer", "hand_click"]:
                # 当事件类型为timer或hand_click时且只有该条件，直接执行任务
                reqInfo += self.do_work(to_log)
            else:  # elif step1["type"] == 'event':
                # 设备上传数据可能 在condition_info里没有condition关键字
                # if not step1.get("condition") or data["event_value"][0]["value"] == step1["condition"][0]["comparison_value"]:
                if not False in DeviceStatus.opera(step1["condition"], data["event_value"]):
                    reqInfo += self.do_work(to_log)
        elif not step1.get("condition") or (not False in DeviceStatus.opera(step1["condition"], data["event_value"])):
            # 获取场景触发所需条件
            status_list = [item for item in condition_info if item["type"] == "status"]
            result_key = "sc:{}:result".format(self.smart_id)
            result = {}
            for status in status_list:
                condition = status["condition"]
                para = []
                for item in condition:
                    para.append({"name": item["parameter_name"], "value": item["comparison_value"]})
                status["condition"] = json.dumps(condition)
                # 暂存需要满足的条件，等设备返回状态， 设备返回到get_device_status_value_resp服务
                key = "sc:{}:{}".format(self.smart_id, status["status_id"])
                status.setdefault("smart_id", self.smart_id)
                redisdb("hmset", key, status)
                redisdb("expire", key, 15)
                result.update({status["status_id"]: '0'})
                # result.setdefault(status["status_id"], '0')

                # 获取设备状态
                target_id = status.get("parent_device_id") or status["device_id"]
                resp = {
                    "from_type": "server_event",  # settings.EVENT_SERVER_TOPIC[0][10:-1],
                    "from_id": "",
                    "to_type": "device",
                    "to_id": target_id,
                    "cmd": "get_device_status_value",
                    "parent_device_id": status["parent_device_id"],
                    "status_id": status["status_id"],
                    "status_name": status["status_name"],
                    "device_type_id": status["device_type_id"],
                    "device_id": status["device_id"],
                    "parameter": para
                }
                reqInfo.append(("cloudring/device/{}".format(target_id), resp))
            redisdb("hmset", result_key, result)
            redisdb("expire", result_key, 15)
        else:
            print("do not exe :models.sm.execute")
        return reqInfo

    def execute_function(self, item):
        '''返回执行相关的json'''
        cmd = {
            "from_type": "server_event",
            "from_id": "",
            "to_type": "device",
            "to_id": item["parent_device_id"],
            "cmd": "device_function",
            "parent_device_id": item["parent_device_id"],
            "device_id": item["device_id"],
            "function_name": item.get("function_name", ""),
            "function_id": item["function_id"],
            "parameter": item["parameter"]
        }

        if item["parent_device_id"]:
            cmd.update({"to_id": item["parent_device_id"]})
        else:
            cmd.update({"to_id": item["device_id"]})

        return settings.EVENT_SERVER_TOPIC[0], cmd

    def push_msg(self, item, to_log=None):
        '''极光推送'''
        device_token = TabDeveloper.get_device_token(self.user_id)
        msg = {
            "from_type": "server_event",
            "from_id": "",
            "to_type": "user",
            "to_id": self.user_id,
            "cmd": "user_notice_msg",
            "msg_type": "3",
            "notice_msg": "推送手机通知",
            "pay_load": ""
        }
        ret = user_notice_msg(json.dumps(msg).encode(
            "utf8"), [device_token], [self.user_id])
        if ret.get('Errormsg') == 'success' and ret.get("Code") == "0":
            if to_log:
                to_log.info("推送成功 -- > device_token: {} user_id: {}\t推送的消息 --> {}".format(device_token, self.user_id, msg))
        else:
            if to_log:
                to_log.info("推送失败 -- > device_token: {} user_id: {}\t失败原因 --> {}\t推送的消息 --> {}".format(device_token, self.user_id, ret["Errormsg"],msg))

    def sleep_work(self, item):
        '''延时执行, 定时调用eventserver.api 中sleep_work'''
        now = datetime.now()
        delay_time = item["time"].split(":")
        seconds = int(delay_time[-1])
        if len(delay_time) > 1:
            minutes = int(delay_time[-2])
        else:
            minutes = 0
        if len(delay_time) > 2:
            hours = int(delay_time[-3])
        else:
            hours = 0
        workTime = now + timedelta(hours=hours) + timedelta(minutes=minutes) + timedelta(seconds=seconds)
        workTime = workTime.strftime("%Y-%m-%d %H:%M:%S")
        action_info = {
            "from_type": "user",
            "from_id": self.user_id,
            "to_type": settings.EVENT_SERVER_TOPIC[0][10:-1],
            "to_id": "",
            "cmd": "sleep_work",
            "work_list": json.loads(self.control_info),
            "step": item["step"],
            "smart_id": self.smart_id
        }
        add_timer_data = {
            # "from_type": "server/event/1.0",
            "from_type": settings.EVENT_SERVER_TOPIC[0][10:-1],  # server/event/1.0/  去除cloudring/ 和末尾斜杠
            "from_id": "",
            "to_type": "server_timer",
            "to_id": "",
            "cmd": "add_timer",
            "user_id": self.user_id,
            "timer_id": get_uuid(),
            "timer_name": self.name,
            "action_name": "",
            "action_time": workTime,
            "cycle_type": '0',
            "cycle_parameter": '0000000',
            "action_info": json.dumps(action_info)
        }
        # return "cloudring/server/timer/1.0/", add_timer_data
        return settings.TIMER_SERVER_TOPIC[0], add_timer_data

    def do_work(self, to_log=None):
        """
        执行control_info
        1. sleep --> sleep_work
        2. push --> push_msg
        3. function --> execute_function
        """
        reqInfo = []
        if not self.control_info:
            raise Exception("The smart_control without control_info !")
        work_list = json.loads(self.control_info)
        #[{u'device_icon_url': u'http://adsys.cloudring.net/28a3a853231a448288a6c58811212e51.png', u'parameter': [{u'name': u'\u8def', u'value': u'3'}], u'parent_device_id': u'bda01ad00059', u'device_name': u'\u4e09\u8def\u5f00\u5173', u'function_name': u'\u6253\u5f00', u'control_name': u'\u4e09\u8def\u5f00\u5173-\u6253\u5f00-3', u'device_type_id': u'7a5cad9d63784632884b5fd57ea0567a', u'function_id': u'a91757b8febc42d497f99ffbfae6b65b', u'type': u'function', u'device_id': u'000d6f000b5cf625'}]
        try:
            work_list.sort(key=lambda key: key["step"])  # control_info的 step 字段缺少
        except:
            print traceback.format_exc()
        for item in work_list:
            if item["type"] == "sleep":
                reqInfo.append(self.sleep_work(item))
                break
            if item["type"] == "push":
                self.push_msg(item, to_log)
            if item["type"] == "function":
                reqInfo.append(self.execute_function(item))
        return reqInfo


class GroupBroadcast(models.Model):
    group_id = models.CharField(primary_key=True, max_length=32)
    group_name = models.CharField(max_length=256)
    client_id = models.CharField(unique=True, max_length=32)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)

    class Meta:
        db_table = "group_broadcast"


class UserFamily(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    family_id = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32)
    nice_name = models.CharField(max_length=256)
    is_master = models.IntegerField(default=0)
    mobile = models.CharField(max_length=20)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    distinguish_type = models.IntegerField(default=1)

    class Meta:
        db_table = "tab_my_family"


class TabDeveloper(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    account = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20)
    image_url = models.CharField(max_length=250)
    app_id = models.CharField(max_length=32, default=settings.ACCOUNT_TYPE)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=0)
    unusual = models.IntegerField(default=0)
    password = models.CharField(max_length=50)
    class Meta:
        db_table = "tab_developer"

    @classmethod
    def get_device_token(cls, user_id):
        """  获取device_token """
        return redisdb('hget', 'push_' + user_id, 'device_token')

    @property
    def device_token(self):
        return self.get_device_token(self.id)

    def share_device(self, user_id, update_voice_control_func, *args):
        device_list = User_Device.objects.filter(
            user_id=self.id, state=1, owner=1)
        for device in device_list:
            ud = User_Device.objects.filter(
                user_id=user_id, device_id=device.device_id)
            if ud and ud.filter(state=0):
                # 以下代码更新会有错误
                # IntegrityError: (1062, "Duplicate entry '10b3b04d5aa4471b8035f4322125858f-FGWG0100010' for key 'PRIMARY'")
                # ud_in_db = ud.filter(state=0)[0]
                # ud_in_db.state = 1
                # ud_in_db.device_name = device.device_name
                # ud_in_db.save(force_update=True)
                ud.filter(state=0).delete()

            add_ud = User_Device(
                user_id=user_id,
                device_id=device.device_id,
                device_name=device.device_name,
                device_type_id=device.device_type_id,
                state=1
            )
            add_ud.save(force_insert=True)
            voice_data = dict(
                user_id = user_id,
                device_id = device.device_id,
                cmd = "add_device",
                parent_device_id = "",
                language = args[1].get("language", "CN")
            )
            update_voice_control_func(args[0], voice_data)


class TabNews(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    developer_id = models.CharField(max_length=32)
    title = models.CharField(max_length=50)
    content = models.TextField()
    state = models.IntegerField(default=0)
    source = models.CharField(max_length=10)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tab_news"

    def __unicode__(self):
        return self.id


class UserFavoriteRadio(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    user_id = models.CharField(max_length=32)
    device_id = models.CharField(max_length=32)
    parent_device_id = models.CharField(max_length=32)
    device_type_id = models.CharField(max_length=32)
    radio_id = models.CharField(max_length=32)
    state = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_favorite_radio"


class UserSongList(models.Model):
    list_id = models.CharField(primary_key=True, unique=True, max_length=200)
    user_id = models.CharField(max_length=32)
    list_name = models.CharField(max_length=32)
    list_type = models.CharField(max_length=1)
    song_count = models.CharField(max_length=5)
    list_cover = models.CharField(max_length=256)
    state = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_song_list"


class SongListInfo(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    list_id = models.CharField(max_length=200)
    album_id = models.CharField(max_length=32)
    track_id = models.CharField(max_length=32)
    state = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "song_list_info"


class UserFavoriteSong(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    user_id = models.CharField(max_length=32)
    album_id = models.CharField(max_length=32)
    track_id = models.CharField(max_length=32)
    state = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_favorite_song"


class ClientLoginLog(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    time = models.DateTimeField(auto_now=True)
    client_id = models.CharField(max_length=32)
    client_type = models.IntegerField(default=0)
    client_type_id = models.CharField(max_length=32)
    state = models.IntegerField(default=0)
    IP = models.CharField(max_length=32)

    class Meta:
        db_table = "client_login_log"


class ClientLoginInfo(models.Model):
    client_id = models.CharField(primary_key=True, unique=True, max_length=32)
    client_type = models.IntegerField(default=0)
    client_type_id = models.CharField(max_length=32)
    active_time = models.DateTimeField(auto_now=True)
    time = models.DateTimeField(auto_now=True)
    IP = models.CharField(max_length=32)
    area = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    state = models.IntegerField(default=0)

    class Meta:
        db_table = "client_login_info"


class ClientActiveInfo(models.Model):
    client_id = models.CharField(primary_key=True, unique=True, max_length=32)
    client_type = models.IntegerField(default=0)
    client_type_id = models.CharField(max_length=32)
    active_time = models.DateField(auto_now=True)

    class Meta:
        db_table = "client_active_info"


class IpAreaProvinceCity(models.Model):
    ip = models.CharField(primary_key=True, unique=True, max_length=32)
    area = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    city = models.CharField(max_length=32)

    class Meta:
        db_table = "ip_area_province_city"


class CityTimeZone(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    country = models.CharField(max_length=32)
    city_en = models.CharField(max_length=32)
    city_cn = models.CharField(max_length=32)
    time_zone = models.CharField(max_length=10)

    class Meta:
        db_table = "city_time_zone"


class CountryTzDst(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    country_en = models.CharField(max_length=32)
    country_cn = models.CharField(max_length=32)
    dst_start_date = models.CharField(max_length=32)
    dst_end_date = models.CharField(max_length=32)
    year_of_date = models.CharField(max_length=32)

    class Meta:
        db_table = "country_tz_dst"


class IpCountryCity(models.Model):
    ip = models.CharField(primary_key=True, unique=True, max_length=32)
    country_en = models.CharField(max_length=32)
    city_en = models.CharField(max_length=32)

    class Meta:
        db_table = "ip_country_city"


class FirmWareVersion(models.Model):
    id = models.IntegerField(primary_key=True)
    device_type_id = models.CharField(max_length=32)
    version_name = models.CharField(max_length=255)
    firmware_url = models.CharField(max_length=255)
    firmware_url1 = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=255)
    state = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "firmware_version"

    def get_firmware_url(self):
        if self.firmware_url is not None and self.firmware_url != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""

    def get_firmware_url1(self):
        if self.firmware_url1 is not None and self.firmware_url1 != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""

class FirmWareVersionDE(models.Model):
    id = models.IntegerField(primary_key=True)
    device_type_id = models.CharField(max_length=32)
    version_name = models.CharField(max_length=255)
    firmware_url = models.CharField(max_length=255)
    firmware_url1 = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=255)
    state = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "firmware_version_de"

    def get_firmware_url(self):
        if self.firmware_url is not None and self.firmware_url != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""

    def get_firmware_url1(self):
        if self.firmware_url1 is not None and self.firmware_url1 != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""

class FirmWareVersionEN(models.Model):
    id = models.IntegerField(primary_key=True)
    device_type_id = models.CharField(max_length=32)
    version_name = models.CharField(max_length=255)
    firmware_url = models.CharField(max_length=255)
    firmware_url1 = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=255)
    state = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "firmware_version_en"

    def get_firmware_url(self):
        if self.firmware_url is not None and self.firmware_url != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""

    def get_firmware_url1(self):
        if self.firmware_url1 is not None and self.firmware_url1 != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""

class FirmWareVersionFR(models.Model):
    id = models.IntegerField(primary_key=True)
    device_type_id = models.CharField(max_length=32)
    version_name = models.CharField(max_length=255)
    firmware_url = models.CharField(max_length=255)
    firmware_url1 = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=255)
    state = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "firmware_version_fr"

    def get_firmware_url(self):
        if self.firmware_url is not None and self.firmware_url != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""

    def get_firmware_url1(self):
        if self.firmware_url1 is not None and self.firmware_url1 != "":
            return settings.QI_NIU_URL1 + self.firmware_url
        return ""


class TabVoice(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=32)
    device_type_id = models.CharField(max_length=50)
    voice_content = models.CharField(max_length=900)
    state = models.IntegerField()
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    update_user = models.CharField(max_length=32)
    create_user = models.CharField(max_length=32)

    class Meta:
        db_table = "tab_voice"


class UserRoom(models.Model):
    # id = models.CharField(primary_key=True, unique=True, max_length=32)
    room_id = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32)
    room_name = models.CharField(max_length=45)
    sort_no = models.IntegerField(max_length=11, default=0)
    state = models.IntegerField(max_length=11, default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_room"
        unique_together = (("room_id", "user_id"),)


class User_Transaction(models.Model):
    id = models.CharField(max_length=32,primary_key=True)
    user_id = models.CharField(max_length=32)
    device_id = models.CharField(max_length=32)
    device_type_id = models.CharField(max_length=32)
    topic = models.CharField(max_length=256)
    type = models.SmallIntegerField(default=0)
    content = models.CharField(max_length=256)
    status = models.SmallIntegerField(default=1)
    weekday = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    member = models.CharField(max_length=256)
    remark = models.CharField(max_length=32)
    state = models.IntegerField(max_length=11, default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "user_transaction"