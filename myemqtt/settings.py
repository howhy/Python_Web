# -*- coding: utf-8 -*-
#-*- coding:utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
##数据库连接参数
DATABASES = {
    'default': {
            'ENGINE': 'mysql+pymysql',
            'NAME':'cloudringdb',
            'USER': 'root',
            'PASSWORD': 'howhy@123',
            'HOST': 'localhost',
            'PORT': '3306',
    }
}
##emqtt设置
############emqtt 服务器参数#################
EMQTT_HOST='192.168.1.185'
EMQTT_TCP_PORT=1883
############emqtt WEB API参数#################
EMQTT_WEB_PORT=18083
EMQTT_WEB_USERNAME='admin'
EMQTT_WEB_PASSWORD='public'
############cloudring/server/user/1.2/CN/#################
EMQTT_USER_USERNAME='user_cn'
EMQTT_USER_PASSWORD='123456'
