from machine import Pin

class DHTT:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)
            
    def getdata(self):        
        print(self.pin.value())
        
        return (self.pin.value())
    
        