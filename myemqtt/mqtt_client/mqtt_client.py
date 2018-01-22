# -*- coding: utf-8 -*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import logging
from logging import handlers
from hbmqtt.client import MQTTClient,ConnectException
from hbmqtt.mqtt.constants import QOS_0,QOS_1, QOS_2
import settings

class Mqtt_Client(object):
    def __init__(self,app):
        self.server=settings.EMQTT_HOST
        self.port=settings.EMQTT_TCP_PORT
        self.username=settings.EMQTT_USER_USERNAME
        self.password=settings.EMQTT_USER_PASSWORD
        self.qos=QOS_0
        self.mqttclient=MQTTClient(client_id="cloudring-server-user")
        self.app=app

    def connect(self):
        try:
            self.logginger().info("Connect()==>success [server={}][port={}][clientid={}][username={}][password={}]".format(self.server, self.port, self.mqttclient.client_id, self.username, self.password))
            return self.mqttclient.connect("mqtt://{username}:{password}@{server}:{port}".format(username=self.username,password=self.password,server=self.server,port=self.port))
        except ConnectException as err:
            self.logginger('error').error("Connect()==>fail [server={}][port={}][clientid={}][username={}][password={}][errors={}]".format(self.server, self.port, self.mqttclient.client_id, self.username, self.password,err))
            self.mqttclient.reconnect()
    def reconnect(self):
        return self.mqttclient.reconnect()

    def subscribe(self,*topic):
        return self.mqttclient.subscribe(topic)

    def publish(self,topic,payload_json):
        return self.mqttclient.publish(topic,payload_json,retain=None,qos=self.qos)

    def deliver_message(self):
        return self.mqttclient.deliver_message()

    def logginger(self,level='info'):
        appdir=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),self.app)
        loger = logging.Logger(self.app, level=logging.DEBUG)
        logfile={'debug':'log/debug.log','info':'log/info.log','error':'log/error.log'}
        fh = logging.handlers.RotatingFileHandler(os.path.join(appdir,logfile.get(level)),maxBytes=2048000,backupCount=1)
        formatter = logging.Formatter("%(asctime)s %(name)s [%(filename)s:%(lineno)d] %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        loger.addHandler(fh)
        return loger




