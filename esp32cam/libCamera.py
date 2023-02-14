import camera
from machine import Pin
from time import sleep
import time
import uos
from machine import SDCard


led = Pin(4, Pin.OUT)

class CAMERA:
    def __init__(self, framesize=10, save_path='/sd/', debug='1'):
        camera.init()
        camera.framesize(framesize)     # frame size 10: 800X600 (1.33 espect ratio)
        camera.contrast(2)       # increase contrast
        camera.speffect(0)       # 0-->color , 2 -->jpeg grayscale
        
        self.save_path = save_path
        self.debug = debug
        
    def get_img(self, flash='0'):
        if flash=='1':
            led.value(1)
            sleep(0.15)
            
        img = camera.capture()
        led.value(0)
        
        return img
        
    def restart(self):
        camera.deinit()
        sleep(1)
        camera.init()
        camera.framesize(10)     # frame size 800X600 (1.33 espect ratio)
        camera.contrast(2)       # increase contrast
        camera.speffect(0)       # 0-->color , 2 -->jpeg grayscale
    
    def mount_sd(self):
        uos.mount(SDCard(),'/sd')
        uos.chdir('sd')
        uos.listdir()
        
    def take_picture(self, flash='1'):
        img = self.get_img(flash)
        
        now_path = None
                   
        nowtime = time.localtime(time.mktime(time.localtime())+28800)
            
        now_file = '-'.join([ str(x) for x in nowtime[:6] ]) + '.jpg'
        now_path = self.save_path + now_file
        uos.chdir('/sd')
        uos.listdir()
            
        with open(now_path, "wb") as imgFile:
            imgFile.write(img)
        
        return img, now_path

    def led_flash(self, count=3, ftime=(0.25,0.5)):
        led.value(0)
        for i in range(0,count):
            led.value(1)
            sleep(ftime[0])
            led.value(0)
            if ftime[1]>0:
                sleep(ftime[1])

    def release(self):
        camera.deinit()