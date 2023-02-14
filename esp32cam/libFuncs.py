import uos
from machine import SDCard

def mount_sd():
    uos.mount(SDCard(slot=2, sck=14, miso=2, mosi=15, cs=13), "/sd")
    #uos.mount(SDCard(),'/sd')
    uos.chdir('sd')
    uos.listdir()



