import network
from time import sleep
import ntptime
import time

class WIFI:
    def __init__(self, ssid, pwd):
        self.ssid = ssid
        self.pwd = pwd
        self.wifi = network.WLAN(network.STA_IF)
        
    def connect_wifi(self, retry=3, reconnect=3, wait=1):
        wifi = self.wifi
        conn_status = False
        
        for i in range(0, reconnect):
            wifi.active(False) # break any existing connection
            wifi.active(True)
            wifi.config(reconnects = retry) # 5 tries max
            
            try:
                wifi.connect(self.ssid, self.pwd)
            except OSError as e:
                print('Cannot connect WIFI: ', e)
            
            if wifi.isconnected():
                conn_status = True
                print('connected', wifi.ifconfig())
                break
            
            else:
                print('connect failed')
            
            sleep(wait)
            
        return conn_status

    def check_connect(self):
        wifi = self.wifi
        return wifi.isconnected()

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
