import paho.mqtt.client as mqtt
import cv2
import json
import os, time
import keyboard
import threading
from configparser import ConfigParser
import ast
import binascii

cfg = ConfigParser()
cfg.read("config.ini",encoding="utf-8")

def on_connect(client, userdata, flags, rc):
    for topic_sub in ast.literal_eval(cfg.get("MQTT", "MQTT_SUB_TOPIC")):
        print("Subscribe to", topic_sub)
        client.subscribe(topic_sub)

def display_msg(client_name, img):
    save_folder = os.path.join('recv', client_name)
    if not os.path.exists( save_folder): os.makedirs(save_folder)

    win_name = client_name
    saved_path = os.path.join(save_folder, '{}.jpg'.format(str(time.time())))
    
    with open(saved_path, "wb") as f:
        f.write(img)
    
    cv2.imshow(win_name, cv2.imread(saved_path))     
    # 當接收到從伺服器發送的圖片後，儲存下來接著顯示15秒鐘後再關閉視窗。         
    cv2.waitKey(cfg.getint("GLOBAL","seconds_display"))    
    cv2.destroyWindow(win_name)  

    if cfg.getboolean("GLOBAL","save_local") is False:
        os.remove(saved_path)

    

def on_message(client, userdata, msg):    
    print('received msg')
    data_rcv = json.loads(msg.payload)
    cam_name = data_rcv["client"]
    print('client', client)
    img = binascii.a2b_base64(data_rcv["image"])
    #print("client", client)
    t = threading.Thread(target=display_msg, args=(cam_name, img, ))
    t.start()

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