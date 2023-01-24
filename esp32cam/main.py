from libFuncs import *
from libMQTT import MQTT
from libCamera import CAMERA
import time

mount_sd()

#file = open ("/sd/wifi_info.txt", "w")
#file.write( "TsengChengHsun (6125)\n")
#file.write( "iwanttosee\n")
#file.write( "Redmi\n")
#file.write( "hospital\n")
#file.close()


file_path = "/sd/wifi_info.txt"
with open(file_path, 'r') as f:
    lines = f.readlines()

if len(lines)>=12:
    WIFI_AP = lines[0].replace('\n','').replace('\r','').split(':')[1]
    WIFI_PWD = lines[1].replace('\n','').replace('\r','').split(':')[1]
    MQTT_HOST = lines[2].replace('\n','').replace('\r','').split(':')[1]
    MQTT_PORT = int(lines[3].replace('\n','').replace('\r','').split(':')[1])
    MQTT_USR = lines[4].replace('\n','').replace('\r','').split(':')[1]
    MQTT_PWD = lines[5].replace('\n','').replace('\r','').split(':')[1]
    MQTT_SUB_TOPIC = lines[6].replace('\n','').replace('\r','').split(':')[1]
    MQTT_PUB_TOPIC = lines[7].replace('\n','').replace('\r','').split(':')[1]
    CAM_NAME = lines[8].replace('\n','').replace('\r','').split(':')[1]
    SAVE_TO_SD = lines[9].replace('\n','').replace('\r','').split(':')[1]
    txt_take_pic = lines[10].replace('\n','').replace('\r','').split(':')[1]
    txt_take_flash_pic = lines[11].replace('\n','').replace('\r','').split(':')[1]
    print('MQTT_SUB_TOPIC', MQTT_SUB_TOPIC)
    conn_status = retry_wifi_connect(WIFI_AP, WIFI_PWD, retry=5, wait=3)
    print('conn_status', conn_status)
    
    if conn_status is True:        
    
        cam = CAMERA()        
        cam.led_flash(count=3, ftime=(0.15,0.25))
            
        mqtt = MQTT(pub_topic=MQTT_PUB_TOPIC, cid=CAM_NAME, host=MQTT_HOST, mqttport=MQTT_PORT, user=MQTT_USR, \
                    pwd=MQTT_PWD, keeplive=5, save_file=SAVE_TO_SD, \
                    txtTake=txt_take_pic, txtFTake=txt_take_flash_pic, objCam=cam) 
        mqtt.subscribe(topic=MQTT_SUB_TOPIC)
        
        while True:
            cam.get_img(flash='0')
            mqtt.check_msg()
            
        
        '''
        _, pic_path = cam.take_picture(save_file=True)

        f=open(pic_path, "rb")
        fileContent = f.read()
        byteArr = bytearray(fileContent)

        mqtt.publish(topic='esp32cam', msg=byteArr)
        '''    
    
else:
    print('wifi_info.txt is not correct:', lines)
    
