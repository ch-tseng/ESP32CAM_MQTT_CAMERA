import paho.mqtt.client as mqtt
import cv2
import os, time
import keyboard
from configparser import ConfigParser
import ast

cfg = ConfigParser()
cfg.read("config.ini",encoding="utf-8")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe( cfg.get("MQTT","MQTT_SUB_TOPIC") )

# 當接收到從伺服器發送的圖片後，儲存下來接著顯示10秒鐘後再關閉視窗。
def on_message(client, userdata, msg):   
    if not os.path.exists('recv'): os.makedirs('recv')

    saved_path = 'recv/{}.jpg'.format(str(time.time()))
    f = open(saved_path, "wb")
    f.write(msg.payload)
    print("Image Received")
    f.close()
    img = cv2.imread(saved_path)
    print(img.shape)
    cv2.imshow('test', img)
    cv2.waitKey(10000)
    cv2.destroyWindow("test")

    if cfg.getboolean("GLOBAL","save_local") is False:
        os.remove(saved_path)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(cfg.get("MQTT", "MQTT_HOST"), cfg.getint("MQTT", "MQTT_PORT"), cfg.getint("MQTT", "MQTT_TIMEOUT"))

client.loop_start()

last_pressed = 0.0
while True:
    if time.time() - last_pressed > 3.0:
        if keyboard.is_pressed('p'):         
            client.publish(cfg.get("MQTT","MQTT_PUB_TOPIC"), cfg.get("GLOBAL", "txt_take_pic"))
            print('Send MQTT to take picture.')
            last_pressed = time.time()

        elif keyboard.is_pressed('f'):         
            client.publish(cfg.get("MQTT","MQTT_PUB_TOPIC"), cfg.get("GLOBAL", "txt_take_flash_pic"))
            print('Send MQTT to take picture with flash.')
            last_pressed = time.time()

client.loop_stop()    