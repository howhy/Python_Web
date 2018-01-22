# -*- coding: utf-8 -*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from mqtt_client.mqtt_client import Mqtt_Client
from hbmqtt.client import ClientException
from hbmqtt.codecs import decode_string,encode_string
from handler import UserServer
@asyncio.coroutine
def main():
    mqtt_client=Mqtt_Client('userserver')
    yield from mqtt_client.connect()
    yield from mqtt_client.subscribe(*[('cloudring/server/user/1.1/CN/', mqtt_client.qos),])
    while 1:
        try:
            message = yield from mqtt_client.deliver_message()
            packet = message.publish_packet
            mqtt_client.logginger().info("Main  Rece-->client_ID=%s Topic=%s  Sub_info=%s" % (mqtt_client.mqttclient.client_id,packet.variable_header.topic_name, str(packet.payload.data,encoding='utf-8')))
            userserver=UserServer(mqtt_client, packet.variable_header.topic_name, str(packet.payload.data,encoding='utf-8'))
            yield from userserver.control()
        except ClientException as ce:
            mqtt_client.logginger('error').error("Client exception: %s" %ce)
            yield from mqtt_client.reconnect()
        except Exception as e:
            mqtt_client.logginger('error').error("userserver server exception: %s" %e)
            yield from mqtt_client.reconnect()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt as e:##按ctrl+c会执行这个语句块
        raise SystemExit('>>>Press Ctrl+C forced exit')