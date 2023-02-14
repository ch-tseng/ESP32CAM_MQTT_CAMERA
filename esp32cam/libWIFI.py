import network
import ubinascii
from time import sleep
import ntptime
import time

class WIFI:
    def __init__(self, ssid, pwd, debug):
        self.ssid = ssid
        self.pwd = pwd
        self.debug = debug
        self.wifi = network.WLAN(network.STA_IF)
        
    def connect_wifi(self, retry=3, reconnect=3, wait=1):
        wifi = self.wifi
        conn_status = False
        
        for i in range(0, reconnect):
            wifi.active(False) # break any existing connection
            wifi.active(True)
            wifi.config(reconnects = retry) # 5 tries max
            
            if self.debug=='1':
                print('MAC Address:', ubinascii.hexlify(wifi.config('mac')).decode())
            try:
                wifi.connect(self.ssid, self.pwd)
            except OSError as e:
                if self.debug == '1':
                    print('Cannot connect WIFI: ', e)
            
            if wifi.isconnected():
                conn_status = True
                if self.debug == '1':
                    print('connected', wifi.ifconfig())
                    
                break
            
            else:
                if self.debug == '1':
                    print('connect failed')
            
            sleep(wait)
            
        return conn_status

    def check_connect(self, print_msg=True):
        wifi = self.wifi
        
        if self.debug == '1':
            if print_msg is True:
                print(wifi.status())
                print("----------------")
                print(wifi.ifconfig())
                print("----------------")
                
        status = wifi.isconnected()
            
        return status

    def tw_ntp(self, host='time.stdtime.gov.tw', must=False):
        #ntptime.NTP_DELTA = 3155644800 # UTC+8 的 magic number
        ntptime.host = host
        count = 1
        if must:
            count = 100
        for _ in  range(count):
            try:
                ntptime.settime()
            except:
                time.sleep(1)
                continue
            else:
                return True
            
        return False
