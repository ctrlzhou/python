# -*- coding:utf8 -*-
import paho.mqtt.client as mqtt
import time

HOST = "119.29.67.174"
PORT = 1883

def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client_id = "17a6948dcecf9b7e"
    client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
    user = "auth_user"
    password = "xxxxxx"
    client.username_pw_set(user, password)  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test")

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))

if __name__ == '__main__':
    client_loop()