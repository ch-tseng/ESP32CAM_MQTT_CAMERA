import urequests
import ujson

class lineNotify:
    def __init__(self, token):
        self.url = "https://notify-api.line.me/api/notify"
        self.token = token

    def sendMSG(self, msg, imgdata=None):
        msg = msg.replace(' ', '%20')
        
        
        
        if imgdata is None:
            headers = {
                "Authorization": "Bearer " + self.token, 
                "Content-Type" : "application/x-www-form-urlencoded"
            }
            
            res = urequests.post(self.url+'?token='+self.token+'&message='+msg, headers=headers)
        else:
            '''
            headers = {
                "Authorization": "Bearer " + self.token, 
                "Content-Type" : "multipart/form-data"
            }
            post_data = ujson.dumps({ 'message': msg, 'imageFile': imgdata})
            #res = urequests.post(self.url+'?token='+self.token+'&message='+msg+'&imageFullsize='+imgdata, headers=headers)
            res = urequests.post(self.url+'?token='+self.token+'&imageFile='+imgdata, headers=headers)
            '''
            post_data = ujson.dumps({ 'imageFile': imgdata})
            headers = { "Authorization": "Bearer " + self.token,  "Content-Type" : "application/x-www-form-urlencoded"}
            res = urequests.post(self.url+'?token='+self.token+'&message='+msg, data=post_data, headers=headers)
        print('response: ', res.text)
        res.close()
