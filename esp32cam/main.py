from libWIFI import WIFI
from libFuncs import *
from libMQTT import MQTT
from libCamera import CAMERA
import time

mount_sd()

file_path = "/sd/wifi_info.txt"
with open(file_path, 'r') as f:
    lines = f.readlines()

if len(lines)>=12:
    WIFI_AP = lines[0].replace('\n','').replace('\r','').split(':')[1].strip()
    WIFI_PWD = lines[1].replace('\n','').replace('\r','').split(':')[1].strip()
    MQTT_HOST = lines[2].replace('\n','').replace('\r','').split(':')[1].strip()
    MQTT_PORT = int(lines[3].replace('\n','').replace('\r','').split(':')[1])
    MQTT_USR = lines[4].replace('\n','').replace('\r','').split(':')[1].strip()
    MQTT_PWD = lines[5].replace('\n','').replace('\r','').split(':')[1].strip()
    MQTT_SUB_TOPIC = lines[6].replace('\n','').replace('\r','').split(':')[1].strip()
    MQTT_PUB_TOPIC = lines[7].replace('\n','').replace('\r','').split(':')[1].strip()
    MQTT_KEEPLIVE = int(lines[8].replace('\n','').replace('\r','').split(':')[1].strip())
    CAM_NAME = lines[9].replace('\n','').replace('\r','').split(':')[1].strip()
    FRAME_SIZE = int(lines[10].replace('\n','').replace('\r','').split(':')[1].strip())
    SAVE_TO_SD = lines[11].replace('\n','').replace('\r','').split(':')[1].strip()
    txt_take_pic = lines[12].replace('\n','').replace('\r','').split(':')[1].strip()
    txt_take_flash_pic = lines[13].replace('\n','').replace('\r','').split(':')[1].strip()
    RETRY_WIFI_CONNECT = int(lines[14].replace('\n','').replace('\r','').split(':')[1].strip())
    FLASH_COUNT_CONNECTED = int(lines[15].replace('\n','').replace('\r','').split(':')[1].strip())
    WIFI_BREAK_WAIT_RECONNECT = int(lines[16].replace('\n','').replace('\r','').split(':')[1].strip())
    print('MQTT_SUB_TOPIC', MQTT_SUB_TOPIC)
    
    cam = CAMERA(framesize=FRAME_SIZE)    
    objWIFI = WIFI(WIFI_AP, WIFI_PWD)
    
    while True:
        _ = objWIFI.connect_wifi(retry=3, reconnect=RETRY_WIFI_CONNECT, wait=2)
        conn_status = objWIFI.check_connect()
        print('conn_status', conn_status)
    
        if conn_status is True:        
            cam.led_flash(count=FLASH_COUNT_CONNECTED, ftime=(0.15,0.25))
            mqtt = MQTT(pub_topic=MQTT_PUB_TOPIC, cid=CAM_NAME, host=MQTT_HOST, mqttport=MQTT_PORT, user=MQTT_USR, \
                        pwd=MQTT_PWD, keeplive=MQTT_KEEPLIVE, save_file=SAVE_TO_SD, \
                        txtTake=txt_take_pic, txtFTake=txt_take_flash_pic, objCam=cam)
            
            mqtt.subscribe(topic=MQTT_SUB_TOPIC + '@{}'.format(CAM_NAME))
            mqtt.subscribe(topic=MQTT_SUB_TOPIC + '@{}'.format('all'))
            
            while conn_status is True:
                #cam.get_img(flash='0')
                mqtt.check_msg()
                
                conn_status = objWIFI.check_connect()
        
        else:
            print("Wifi is disconnected...")
            time.wait(WIFI_BREAK_WAIT_RECONNECT)
            
else:
    print('wifi_info.txt is not correct:', lines)
    
