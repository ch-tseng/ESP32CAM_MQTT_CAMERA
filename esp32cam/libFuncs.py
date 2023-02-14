import uos
from machine import SDCard
import usocket

def mount_sd():
    uos.mount(SDCard(slot=2, sck=14, miso=2, mosi=15, cs=13), "/sd")
    #uos.mount(SDCard(),'/sd')
    uos.chdir('sd')
    uos.listdir()

def chk_resolve(address):
    ip = usocket.getaddrinfo(address,1)[0][-1][0]
    #print('usocket', ip)
    
    try:
        count = len(ip.split('.'))
    except:
        count = 0
        
    if count==4:
        return True
    else:
        return False
    
