from umqtt.robust import MQTTClient
import uos
import time
#from json import dumps
#import binascii

class MQTT:
    def __init__(self, pub_topic, cid, host, mqttport, user, pwd, keeplive=30, save_file='0', txtTake='Take-Picture', \
                 txtFTake='Take-Picture-Flash', objCam=None, debug='0' ):
        if user != '' and pwd != '':
            client = MQTTClient(
                client_id=cid, 
                keepalive=keeplive,
                server=host,
                port=mqttport,
                user=user,
                password=pwd,
                ssl=False)
        else:
            client = MQTTClient(
                client_id=cid, 
                keepalive=5,
                server=host,
                ssl=False)
        
        self.host = host
        self.cid = cid
        self.pub_topic = pub_topic
        self.client = client
        self.objCam = objCam
        self.save_file = save_file
        self.txtTake = txtTake
        self.txtFTake = txtFTake
        self.last_ping = 0
        self.client = client
        self.debug = debug
        
    def mqtt_connect(self, retry=5):
        client = self.client
        conn_status = False
        for i in range(0,5):
            try:
                client.connect(False) # 記得要指定 False                
                conn_status = True
                break
            
            except:
                if self.debug == '1':
                    print("Connect MQTT:{} error".format(self.host))
        
        client.set_callback(self.mqtt_get_msg)
        self.client = client
        return conn_status

    def mqtt_get_msg(self, topic, msg):
        img, now_path = None, None
        
        m = msg.decode('utf-8')
        if m in [self.txtTake, self.txtFTake] and self.objCam is not None:
            
            if m == self.txtFTake:
                _, img_path = self.objCam.take_picture(flash='1')
                
            else:
                _, img_path = self.objCam.take_picture(flash='0')
            
            with open(img_path, "rb") as f:
                fileContent = f.read()
                
            byteArr = bytearray(fileContent)
            
            #jsondata = { "client":self.cid, "image":binascii.b2a_base64(byteArr).decode() }

            self.publish(topic=self.pub_topic, msg=byteArr)
            if self.debug == '1':
                print('Image sent')
            
            if self.save_file == '0':
                uos.remove(img_path)

    def subscribe(self, topic):
        self.topic_sub = topic
        self.client.subscribe(topic)        
        
    def publish(self, topic, msg):
        self.client.publish(topic, msg)
        
    def check_msg(self):
        #try:
        if time.time() - self.last_ping > 20:
            self.last_ping = time.time()
            self.client.ping()
            #print('ping', self.host )
            
        try:
            self.client.check_msg()
            
        except:
            self.mqtt_connect(retry=5)
            self.subscribe(self.topic_sub)