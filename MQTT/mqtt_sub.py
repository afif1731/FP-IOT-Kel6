import json
import requests
import paho.mqtt.client as mqtt

MQTT_BROKER = '152.42.194.14'
MQTT_PORT = 1883
MQTT_TOPIC_BASE = '/iot06/box/'
MQTT_TOPIC = '/iot06/box/+/pub-keypad'

BE_URI = 'http://localhost:4000/secretbox/'

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def keyCheck(keyInput, boxId):
    fullPath = BE_URI + boxId + '/login'
    data = {
        'id': boxId,
        'password': str(keyInput)
    }

    res = requests.post(url=fullPath, json=data)
    # print(res.json())
    json_res = res.json()
    return json_res['status']

def on_message(client, userdata, message):
    boxId = message.topic.split('/')[3]
    rawMsg = str(message.payload.decode("utf-8"))

    if rawMsg != "Null" and rawMsg != "":
        pubTopic = MQTT_TOPIC_BASE + boxId + '/sub-access'
        access = keyCheck(int(rawMsg), boxId)

        if access:
            client.publish(pubTopic, "1")
        else:
            client.publish(pubTopic, "0")
    else:
        client.publish(pubTopic, "0")
    # print("message received " ,str(message.payload.decode("utf-8")))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="admin",password="Kcks1029")
client.connect(MQTT_BROKER, MQTT_PORT, 60 * 60)
client.loop_forever()