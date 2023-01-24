import uos
from machine import SDCard
import network
from time import sleep
import ntptime
import time


def tw_ntp(host='time.stdtime.gov.tw', must=False):
    """
  host: 台灣可用的 ntp server 如下可任選，未指定預設為 clock.stdtime.gov.tw
    tock.stdtime.gov.tw
    watch.stdtime.gov.tw
    time.stdtime.gov.tw
    clock.stdtime.gov.tw  led_flash(
    tick.stdtime.gov.tw
  must: 是否非對到不可
    """
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

def mount_sd():
    uos.mount(SDCard(slot=2, sck=14, miso=2, mosi=15, cs=13), "/sd")
    #uos.mount(SDCard(),'/sd')
    uos.chdir('sd')
    uos.listdir()

def connect_wifi(ssid, pwd, wait=3):
    wifi = network.WLAN(network.STA_IF)
    
    wifi.active(False) # break any existing connection
    wifi.active(True)
    wifi.config(reconnects = 5) # 5 tries max
    #if wifi.isconnected():
    #    return True
    
    wifi.connect(ssid, pwd)

    sleep(wait)
    if wifi.isconnected():
        print('connected', wifi.ifconfig())
        return True
    else:
        print('connect failed')
        return False
    
def connect_wifi2(ssid, pwd, wait=3):
    network.WLAN(network.AP_IF).active(False)
    wifi = network.WLAN(network.STA_IF)
    
    wifi.active(False) # break any existing connection
    wifi.active(True)
    wifi.config(reconnects = 5) # 5 tries max
        
    #if wifi.isconnected():
    #    return True
    
    wifi.connect(ssid, pwd)
    sleep(wait)

    if wifi.isconnected():
        print('connected', wifi.ifconfig())
        return True
    else:
        print('connect failed')
        return False
    
def retry_wifi_connect(ssid, pwd, retry=5, wait=3):
    for i in range(0,retry):
        status = connect_wifi2(ssid, pwd, wait)
        if status is True:
            return True
        
    return False

