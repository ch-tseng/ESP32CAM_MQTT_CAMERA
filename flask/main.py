# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mqtt import Mqtt
import time

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
s_topic = 'IMGS_for_MQTT'
r_topic = 'CMDS_for_MQTT'

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(s_topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       #payload=message.payload.decode()
       payload=message.payload
   )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))
   with open('static/recv.jpg', "wb") as f:
       f.write(message.payload)

@app.route('/')
def home():
   return render_template('home.html', img_path='recv.jpg')

@app.route('/pub', methods=['POST'])
def publish():
   if request.method == 'POST':
      p_value = request.form.get('p_type')
      if p_value is not None:
         print('p_value', p_value)
         publish_result = mqtt_client.publish(r_topic,p_value)
   # return jsonify({'code': publish_result[0]})
   #return render_template("home.html")
   #return redirect(url_for('home'))

   #return render_template('home.html', img_path='recv.jpg')
   return redirect(url_for('home'))

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)
