from libWIFI import WIFI
from libFuncs import *
from libMQTT import MQTT
from libCamera import CAMERA
from time import sleep
from time import time

mount_sd()

file_path = "/sd/wifi_info.txt"
with open(file_path, 'r') as f:
    lines = f.readlines()

if len(lines)>=20:
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
    NTP_HOST = lines[17].replace('\n','').replace('\r','').split(':')[1].strip()
    FLASH_NOTIFY = lines[18].replace('\n','').replace('\r','').split(':')[1].strip()
    DEBUG_PRINT = lines[19].replace('\n','').replace('\r','').split(':')[1].strip()
     
    cam = CAMERA(framesize=FRAME_SIZE, debug=DEBUG_PRINT)    
    objWIFI = WIFI(WIFI_AP, WIFI_PWD, DEBUG_PRINT)
    
else:
    print('wifi_info.txt is not correct:', lines)
    
    while True:
        if FLASH_NOTIFY == '1':
            cam.led_flash(count=FLASH_COUNT_CONNECTED, ftime=(0.15,1.0))
    
# WIFI -----------------------------------------
conn_status = False
network_status = False
last_chk_network = 0

if FLASH_NOTIFY == '1':
    cam.led_flash(count=1, ftime=(1.0,0.5))

while True:
    if conn_status is False or network_status is False:
        if DEBUG_PRINT == '1':
            print("Wifi is disconnected...")
            
        sleep(WIFI_BREAK_WAIT_RECONNECT)
            
        _ = objWIFI.connect_wifi(retry=3, reconnect=RETRY_WIFI_CONNECT, wait=2)
        
        if FLASH_NOTIFY == '1':
            cam.led_flash(count=1, ftime=(1.0,1.0))
            
        conn_status = objWIFI.check_connect(print_msg=True)
        network_status = chk_resolve(MQTT_HOST)
  
    else:
        if FLASH_NOTIFY == '1':
            cam.led_flash(count=FLASH_COUNT_CONNECTED, ftime=(0.1,0.25))
            
        objWIFI.tw_ntp(host=NTP_HOST, must=False)
            
        mqtt = MQTT(pub_topic=MQTT_PUB_TOPIC, cid=CAM_NAME, host=MQTT_HOST, mqttport=MQTT_PORT, user=MQTT_USR, \
                    pwd=MQTT_PWD, keeplive=MQTT_KEEPLIVE, save_file=SAVE_TO_SD, \
                    txtTake=txt_take_pic, txtFTake=txt_take_flash_pic, objCam=cam, debug=DEBUG_PRINT)
        
        
        mqtt_status = mqtt.mqtt_connect(retry=5)
        
        if FLASH_NOTIFY == '1':
            cam.led_flash(count=1, ftime=(1.0,1.0))
        
        if mqtt_status is True:
            if FLASH_NOTIFY == '1':
                cam.led_flash(count=FLASH_COUNT_CONNECTED, ftime=(0.1,0.25))
                
            mqtt.subscribe(topic=MQTT_SUB_TOPIC)

            if DEBUG_PRINT == '1':
                print('Subscribe', MQTT_SUB_TOPIC)
            
            while conn_status is True and network_status is True and mqtt_status is True:
                cam.get_img(flash='0')
                mqtt.check_msg()
                
                if time() - last_chk_network > 60:
                    last_chk_network = time()
                    conn_status = objWIFI.check_connect(print_msg=False)
                    network_status = chk_resolve(MQTT_HOST)
                    mqtt_status = mqtt.mqtt_connect(retry=5)
                
        else:
            if DEBUG_PRINT == '1':
                print("cannot connect to MQTT, Reonnect WIFI and MQTT...")
            
            while mqtt_status is False:
                mqtt_status = mqtt.mqtt_connect(retry=5)            
                sleep(5)
