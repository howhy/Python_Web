# -*- coding: utf-8 -*-
import requests
import json
import traceback
from settings import EMQTT_HOST,EMQTT_WEB_PORT,EMQTT_WEB_PASSWORD,EMQTT_WEB_USERNAME
def mqtt_online(client_id):
    try:
        retInfo = {"IP": "", "state": "0", "update_time": ""}
        url = "http://{host}:{port}/api/v2/clients/{client_id}".format(host=EMQTT_HOST, port=EMQTT_WEB_PORT,client_id=client_id)
        res = requests.get(url, auth=(EMQTT_WEB_USERNAME, EMQTT_WEB_PASSWORD), timeout=5)
        online_info = json.loads(str(res.content,encoding='utf-8'))["result"]["objects"]
        if online_info:
            ret = online_info[0]
            return True, {"IP": ret["ipaddress"], "state": "1", "update_time": ret["connected_at"]}
    except requests.exceptions.ConnectTimeout:
        traceback.format_exc()
    return False, retInfo