# -*- coding: utf-8 -*-
import json
import asyncio
from utils.dbhandler import DBsession,DBHandler
from utils.device_isonline import mqtt_online
from models.models import Device,User_Device,UserRoom,SubDeviceInfo,TabDeveloper,Device_Type,DeviceData,DeviceEvent,DeviceFunction,UserFamily
import uuid
import datetime
import traceback
class UserServer(object):
    def __init__(self,client,topic,payload_json):
        self.client=client
        self.topic=topic
        try:
            self.payload_dict = json.loads(payload_json)
        except ValueError as e:
            self.client.logginger('error').error('userserver control error %s' % traceback.format_exc())


    def data_strip(self,data):
        """ 去除dict中key和value前后的空格 """
        ret_data = {}
        for key in data:
            r_key = key.strip()
            if not isinstance(data[key], dict) and not isinstance(data[key], list):
                ret_data[r_key] = data[key].strip()
            else:
                ret_data[r_key] = data[key]
        return ret_data

    def check_keys(self):
        check = set(["from_type", "from_id", "to_type", "to_id", "cmd"])
        if not check.issubset(self.data_strip(self.payload_dict)):
            self.client.logginger.error("Necessary parameters are not complete: {}".format(self.payload_dict))
            return False
        return True

    @asyncio.coroutine
    def control(self):
        try:
            if self.check_keys():
                resp = {
                    "from_type": "server_user",
                    "from_id": "",
                    "to_type": "user",
                    "to_id": self.payload_dict.get("from_id"),
                    "cmd": self.payload_dict.get("cmd")+'_resp',
                    "error_no": "0",
                    "error_msg": "OK"
                }
                payload_dict=self.data_strip(self.payload_dict)
                cmd=payload_dict.get('cmd')
                if hasattr(self,cmd):
                    # topic,data=getattr(self,cmd)(payload_dict)
                    resp_data=getattr(self,cmd)(payload_dict)
                    #resp.update(data)
                else:
                    topic="cloudring/user/%s"%payload_dict.get("from_id")
                    resp["error_no"]= "1"
                    resp["error_msg"]="cmd error"
                for topic,data in resp_data:
                     resp.update(data)
                     yield from self.client.publish(topic, bytes(json.dumps(resp),encoding='utf-8'))
                #yield from self.client.publish("/test/123", bytes(json.dumps({"test":"dfdsfsdf"}),encoding='utf-8'))
                # self.client.logginger('debug').info(pub_msg)
                self.client.logginger().info('Publish OK-->Topic=%s   Pub_info=%s'%(topic, resp))
        except Exception as e:
            self.client.logginger('error').error('userserver control error %s' % traceback.format_exc())
            self.client.logginger('error').error('userserver control error %s'%e)

    def add_device(self, data):
         try:
             resp = {"device_state": "0"}
             user_device_all=DBHandler(User_Device).query(device_id=data['device_id'])
             device = DBHandler(Device).query(device_id=data['device_id']).first()
             if len(user_device_all.filter_by(user_id=data["user_id"], state=1).all())>0:
                 # 用户拥有使用权限
                 user = DBHandler(TabDeveloper).query(id=data['user_id']).first()
                 user_device = user_device_all.filter_by(user_id=data["user_id"], state=1).first()
                 resp.update({
                     "error_no": "3",
                     "error_msg": "You have added this device. Please do not add it repeatly",
                     "owner_id": data["user_id"],
                     "owner_name": user_device.user_name,
                     "device_name": user_device.device_name,
                     "device_id": data['device_id']
                 })
             elif len(user_device_all.filter_by(state=1).all())>0:
                 # 设备已被其它用户绑定
                 bind_user = user_device_all.filter_by(state=1, owner=1).first()
                 resp.update({
                     "error_no": "2",
                     "error_msg": "Device has been bound!",
                     "owner_id": bind_user.user_id,
                     "owner_name": bind_user.user_name,
                     "device_name": bind_user.device_name,
                     "device_id": data['device_id']
                 })
             elif len(user_device_all.filter_by(user_id=data["user_id"], state=0).all())>0:
                 # 设备未绑定且用户曾经拥有使用该设备使用记录
                 user_device = user_device_all.filter_by(user_id=data["user_id"], state=0).delete()
                 master = User_Device(
                     device_id=device.device_id,
                     device_name=data["device_name"],
                     device_type_id=device.device_type.device_type_id,
                     user_id=data["user_id"],
                     user_name=data["user_name"],
                     update_time = datetime.datetime.now(),
                     owner=1,
                     state=1
                 )
                 DBHandler(master).add()
                 resp.update({
                     "error_no": "0",
                     "error_msg": "OK",
                     "device_name": master.device.device_name,
                     "device_id": data['device_id']
                 })
             else:
                 master = User_Device(
                     device_id=device.device_id,
                     user_id=data["user_id"],
                     update_time = datetime.datetime.now(),
                     owner=1,
                     state=1
                 )
                 DBHandler(master).add()
                 resp.update({
                     "error_no": "0",
                     "error_msg": "OK",
                     "device_name": master.device.device_name,
                     "device_id": data['device_id']
                 })
             if mqtt_online(data["device_id"])[0]:
                 resp.update({"device_state": "1"})
         except Exception as e:
             self.client.logginger('error').error(str(e))
             resp.update({"error_no": "1", "error_msg": "unkown error", "device_id": "", "device_name": ""})
         return "cloudring/user/{}".format(data["from_id"]),resp

    def get_user_device_list(self,data):
        devices = DBHandler(User_Device).query(user_id=data["user_id"], state=1).all()
        devices_list = [{
                "device_id": item.device_id,
                "device_name": item.device_name,
                "device_type_id": item.device.device_type_id ,
                "device_type_name": item.device.device_type.device_name if item.device.device_type else "",
                "picture": item.device.device_type.picture if item.device.device_type else "" ,
                "module": item.device.device_type.model if item.device.device_type else "",
                "control_url": item.device.device_type.control_url if item.device.device_type else "",
                "control_version": item.device.device_type.control_version if item.device.device_type else "",
                "device_version": item.device.device_type.device_version if item.device.device_type else "",
               "connect_type": str(item.device.device_type.connect_type) if item.device.device_type else "",
                "device_state": "1" if mqtt_online(item.device_id)[0] else str(mqtt_online(item.device_id)[1]),
                "is_owner": str(item.owner),
                "is_parent_device": str(item.device.device_type.is_parent_device) if item.device.device_type else ""
            } for item in devices]
        return (("cloudring/user/{}".format(data["from_id"]),{"devices_list":devices_list}))

    def get_system_device_list(self,data):
        device_type_list=DBHandler(Device_Type).query(connect_type=1, state=1, verify_state=1).order_by(Device_Type.create_time).all()
        devices_type_list = [{
            "device_type_id": item.device_type_id,
            "device_name": item.device_name,
            "picture": item.picture,
            "module": item.model,
            "control_url": item.control_url,
            "control_version": item.control_version,
            "device_version": item.device_version,
            "connect_type": item.connect_type,
            "is_parent_device": item.is_parent_device,
            "config_url": item.config_url
            } for item in device_type_list]
        return (("cloudring/user/{}".format(data["from_id"]),{"devices_list":devices_type_list}))

    def get_sub_device_list(self,data):
        device_type_list=DBHandler(Device_Type).query(connect_type=2, state=1, verify_state=1).all()
        device_type_list = [{
            "device_type_id": item.device_type_id,
            "device_name": item.device_name,
            "picture": item.picture,
            "module": item.model,
            "control_url": item.control_url,
            "control_version": item.control_version,
            "device_version": item.device_version,
            "connect_type": item.connect_type,
            "is_parent_device": item.is_parent_device,
            "config_url": item.config_url
            } for item in device_type_list]
        return (("cloudring/user/{}".format(data["from_id"]),{"device_type_list":device_type_list}))

    def get_device_user(self,data):
        user_device_list=DBHandler(User_Device).query(device_id=data["device_id"], state=1).all()
        users_list = [{
            "user_id": item.user_id,
            "user_name": item.user.nick_name,
            "image_url": item.user.image_url,
            "is_owner": item.owner
            } for item in user_device_list]
        return (("cloudring/user/{}".format(data["from_id"]),{"users_list":users_list}))

    # def request_authorize(self,data):
        # user_device = DBHandler(User_Device).query(device_id=data["device_id"], user_id=data["owner_id"], owner=1, state=1).first()
        # if user_device:
        #     state,msg=mqtt_online(data["owner_id"])
        #     if state:
        #         return "cloudring/user/{}".format(data["owner_id"]),{"state":"1"}
        # else:
        #     return "cloudring/user/{}".format(data["from_id"]), {"error_msg": "Please check if owner_id is correct.", "error_no": "1"}

    # def response_authorize(self,data):
    #     user_device = DBHandler(User_Device).query(device_id=data["device_id"], user_id=data["owner_id"]).first()
    #     if user_device:
    #         user_device.update(state=1, owner=0)
    #     else:
    #         device = DBHandler(Device).query(device_id=data["device_id"]).first()
    #         user_device = User_Device(
    #             device_id=device.device_id,
    #             user_id=data["user_id"],
    #             device_type_id=device.device_type_id,
    #             device_name=data["device_name"],
    #             state=1,
    #             # 2017 08 07
    #             parent_device=device
    #         )
    #         DBHandler(user_device).add()
    #     return ("cloudring/user/{}".format(data["user_id"]), data)



    # def delete_device(self,data):
    #     resp={}
    #     try:
    #         user = TabDeveloper.objects.get(id=data["user_id"])
    #         user_device = DBsession.query(User_Device).filter_by(device_id=data["device_id"], user_id=data["user_id"], state=1).first()
    #         if user_device:
    #             # 删除授权
    #             owners = DBsession.query(User_Device).filter_by(device_id=data["device_id"], state=1, owner=1).first()
    #             if owners and owners.user_id == data["user_id"]:
    #                 auth_device = DBsession.query(User_Device).filter_by(device_id=data["device_id"], state=1).filter(User_Device.user_id != data["user_id"]).all()
    #                 auth_user = map(lambda n: n.user_id, auth_device)
    #                 DBsession.query(User_Device).filter_by(device_id=data["device_id"], state=1).filter(User_Device.user_id !=data["user_id"]).update( state=0)
    #                 try:
    #                     device_name = owners.device_name if owners.device_name else auth_device.device_type.device_name
    #                     msg = u"User {} removed the device {}!".format(user.nick_name, device_name)
    #                 except Exception as e:
    #                     self.client.logging_error('device_authorize error %s'%e)
    #             user_device = DBsession.query(User_Device).filter_by(device_id=data["device_id"], user_id=user.id, state=1).update( state=0)
    #         else:
    #             resp.update({"error_no": "2", "error_msg": "The user did not add the device!"})
    #     except Device.DoesNotExist:
    #         resp.update({"error_no": "1", "error_msg": "Device is not exist!"})
    #     return resp

    # def delete_device_authorize_user(self):
    #     pass
    def modify_device_name(self,data):
        pass
        #userroom = DBsession.query(User_Device).filter_by(user_id=data["user_id"], device_id=data["device_id"],state=1).update(device_name=data["device_name"])
    # def add_sub_device(self):
    #     pass
    # def modify_sub_device(self,data):
    #     if not data["device_name"]:
    #         raise KeyError("Sub_device_name can not be null")
    #     resp = { "parent_device_id": data["parent_device_id"], "device_name": data["device_name"] }
    #     sub_device = DBsession.query(SubDeviceInfo).filter_by(device=data["device_id"]).update(device_name=data["device_name"])
    #     # user_device表也做更新 20170804
    #     DBsession.query(User_Device).filter_by(user_id=data["from_id"], parent_device_id=data["parent_device_id"],device=data["device_id"]).update(device_name=data["device_name"])
    #     DBsession.commit()
    #     resp.update({"error_no": "0", "error_msg": "OK", "device_type_id": sub_device[0].device_type_id})
    #     # 添加语音控制关键字
    #     if resp.get("error_no", "-1") == "0":
    #         voice_control.update_voice_control(client, data)
    #     return [("cloudring/user/{}".format(data["from_id"]), resp)]
    #
    def delete_sub_device(self,data):
        try:
            resp = {}
            user_device=DBHandler(User_Device).query(user_id=data["user_id"], device_id=data["parent_device_id"], owner=1,state=1)
            if not user_device:
                resp.update({"error_no": "1", "error_msg": "No permission to delete"})
                return [("cloudring/device/{}".format(data["parent_device_id"]), data)]
            parent_device = DBHandler(Device).query(device_id=data["parent_device_id"])
            return [("cloudring/device/{}".format(data["parent_device_id"]), data)]
        except Device.DoesNotExist:
            resp.update({"error_no": "1", "error_msg": "Device is not exist!"})
        return "cloudring/user/{}".format(data["from_id"]), resp

    def get_sub_device(self,data):
        resp = {}
        if data.get("user_id"):
            resp.update({"user_id": data["user_id"]})
        try:
            devices = DBHandler(SubDeviceInfo).query(parent_device_id=data["device_id"], state=1).all()
            device_list = [{
                    "parent_device_id": data["device_id"],
                    "device_id": item.device_id,
                    "device_name": item.device.device_name,
                    "device_type_id": item.device.device_type_id,
                    "device_name": item.device.device_type.device_name,
                    "picture": item.device.device_type.picture,
                    "module": item.device.device_type.model,
                    "control_url": item.device.device_type.control_url,
                    "control_version": item.device.device_type.control_version,
                    "device_version": item.device.device_type.device_version,
                    "connect_type": str(item.device.device_type.connect_type),
                } for item in devices]
            resp.update({
                "parent_device_id":data["device_id"],
                "sub_device_list": device_list,
                "error_msg": "OK",
                "error_no": "0"
            })
            return "cloudring/user/{}".format(data["from_id"]), resp
        except Exception as e:
            resp.update({"error_no": "1", "error_msg": e})
            return "cloudring/user/{}".format(data["from_id"]), resp

    # def get_sub_device_status(self):
    #     pass
    def get_family_info(self,data):
        familys = DBHandler(UserFamily).query(user_id=data["user_id"], state=1)
        family_list = DBsession.query(UserFamily).filter(UserFamily.id.in_(familys), UserFamily.state==1,UserFamily.distinguish_type!=2).all()
        members_list=[{
                "family_id": item.family_id,
                "user_id": item.user.id,
                "is_master": item.is_master,
                "user_name": item.user.nick_name,
                "user_mobile_phone": item.user.mobile
            } for item in family_list]
        return "cloudring/user/{}".format(data["from_id"]), {"family_list":members_list}

    # def add_family_member(self):
    #     pass
    # def delete_family_member(self):
    #     pass
    # def quit_family_member(self):
    #     pass
    def get_device_event_info(self,data):
        device_type_ids = [device_type["device_type_id"] for device_type in data["device_type"]]
        deviceevents = DBsession.query(DeviceEvent).filter(DeviceEvent.device_type_id.in_(device_type_ids),DeviceEvent.state == 1, DeviceEvent.is_public == 1).all()
        deviceevent_list = [{
            "device_type_id": item.device_type_id,
            "event_id": item.event_id,
            "event_name": item.name,
            "trigger_type ":"",
            "trigger_parameter": [],
            "instruction": item.instruction
        } for item in deviceevents]
        return "cloudring/user/{}".format(data["from_id"]), {"event_list": deviceevent_list}

    def get_device_function_info(self,data):
        device_type_ids = [device_type["device_type_id"] for device_type in data["device_type"]]
        devicefunctions = DBsession.query(DeviceFunction).filter(DeviceFunction.device_type_id.in_(device_type_ids),DeviceFunction.state == 1, DeviceFunction.is_public == 1).all()
        devicefunction_list = [{
            "device_type_id": item.device_type_id,
            "function_id": item.function_id,
            "function_name": item.name,
            "parameter_format": [],
            "instruction": item.instruction
        } for item in devicefunctions]
        return "cloudring/user/{}".format(data["from_id"]), {"function_list": devicefunction_list}

    def get_device_data_info(self,data):
        """{"from_type": "user", "from_id": "01dc05f5e3204c5c9577838fd5c4dec1", "to_type": "server_user", "to_id": "",
         "cmd": "get_device_data_info", "device_type": [{"device_type_id": "5be6bbfdcc454e32b5c9fd12f185be14"}]}"""
        device_type_ids = [device_type["device_type_id"] for device_type in data["device_type"]]
        device_data=DBsession.query(DeviceData).filter(DeviceData.device_type_id.in_(device_type_ids),DeviceData.state==1,DeviceData.is_public==1).all()

        device_data_list=[{
                        "device_type_id":item.device_type_id ,
                        "data_id": item.data_id ,
                        "data_name":item.name ,
                        "value_describe": [],
                        "instruction": item.instruction
                         } for item in device_data ]
        return "cloudring/user/{}".format(data["from_id"]), {"data_list":device_data_list}

    def get_device_info(self,data):
        device=DBsession.query(Device).filter_by(device_id=data['device_id']).first()
        if device.device_type:
            device_info={
                            "device_id": device.device_id,
                            "device_type_id": device.device_type_id,
                            "device_name": device.device_type.device_name,
                            "picture": device.device_type.picture,
                            "module": device.device_type.model,
                            "control_url": device.device_type.control_url,
                            "control_version": device.device_type.control_version,
                            "device_version": device.device_type.device_version,
                            "connect_type": device.device_type.connect_type,
                            "is_parent_device": device.device_type.is_parent_device,
                             "device_state": "1" if mqtt_online(data['device_id'])[0] else mqtt_online(data['device_id'])[1],
                            "error_no": "0",
                            "error_msg": "Success"
                       }
        else:
            device_info={"error_no": "1", "error_msg": "device has not device_type_info"}
        return "cloudring/user/{}".format(data["from_id"]), device_info

    # def get_broadcast(self,data):
    #     pass
    #     # resp = {"cmd": "get_broadcast_resp", "from_type": data['to_type'], "from_id": data[
    #     #     'to_id'], "to_type": data['from_type'], "to_id": data['from_id']}
    #     #
    #     # group_broadcast = GroupBroadcast.objects.filter(
    #     #     client_id=data['user_id']).values("group_name")
    #     #
    #     # if group_broadcast:
    #     #     resp.update({"broadcast_list": list(group_broadcast),
    #     #                  "error_no": "0", "error_message": "Success"})
    #     # else:
    #     #     resp.update({"broadcast_list": list(group_broadcast),
    #     #                  "error_no": "1", "error_message": "No broadcast information to subscribe"})
    #     # return [("cloudring/user/{}".format(data["from_id"]), resp)]
    # def add_timer(self,data):
    #     return [("cloudring/server/timer/1.0/", data)]
    #
    # def modify_timer(self,data):
    #     return [("cloudring/server/timer/1.0/", data)]
    #
    # def delete_timer(self,data):
    #     return [("cloudring/server/timer/1.0/", data)]
    #
    # def user_notice_msg(self):
    #     pass
    def get_user_room(self,data):
        urs = DBsession.query(UserRoom).filter_by(user_id=data["user_id"], state=1)
        room_list = [{"room_id": ur.room_id, "room_name": ur.room_name} for ur in urs]
        resp={"user_id": data["user_id"],"room_list": room_list}
        return "cloudring/user/{}".format(data["from_id"]), resp

    def add_user_room(self,data):
        room_id = str(uuid.uuid1()).replace("-", "")
        #user=DBsession.query(User).filter_by(id=data["user_id"], state=1).first()
        new_userroom=UserRoom(room_id=room_id,user_id=data["user_id"], room_name=data["room_name"],sort_no=data.get("sort_no",0),state=1)
        DBsession.add(new_userroom)
        DBsession.commit()
        resp={"user_id": data["user_id"], "room_id": room_id,"room_name": data["room_name"],"sort_no": data.get("sort_no",0),"family_id": ""}
        return "cloudring/user/{}".format(data["to_id"]), resp

    def modify_user_room(self,data):
        userroom = DBsession.query(UserRoom).filter_by(user_id=data["user_id"], room_id=data["room_id"], state=1).update(dict(room_name = data.get("room_name",''),sort_no = data.get("sort_no",0)))
        DBsession.commit()
        resp={"user_id": data["user_id"],"room_id": data["room_id"],"room_name": data["room_name"],"family_id": ""}
        return "cloudring/user/{}".format(data["to_id"]), resp

    def delete_user_room(self,data):
        userroom=DBsession.query(UserRoom).filter_by(user_id=data["user_id"], room_id=data["room_id"], state=1)
        roomname=userroom.first().room_name
        userroom.update(dict(state=0))
        DBsession.commit()
        resp={ "user_id": data["user_id"],"room_id": data["room_id"],"room_name": roomname}
        return "cloudring/user/{}".format(data["from_id"]), resp

    def modify_device_room(self,data):
        uds = DBsession.query(UserRoom).filter_by(user_id=data["user_id"], device_id=data["device_id"], state=1).update( room_id=data["room_id"]).first()
        room_name = uds[0].room.room_name
        resp={"user_id": data["user_id"],"device_id": data["device_id"],"room_id": data["room_id"],"room_name": room_name}
        return "cloudring/{}/{}".format(data["to_type"], data["to_id"]), resp