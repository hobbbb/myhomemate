import json
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    client.subscribe('myhome/#')


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
    except Exception:
        data = msg.payload.decode()
    print(f'{msg.topic} {data}')


mqtt_client = mqtt.Client('myhome')
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect('localhost')


def publish_event(event, data=None):
    msg = ''
    if type(data) is dict:
        msg = json.dumps(data)
    else:
        msg = data
    mqtt_client.publish(f'myhome/{event}', msg)
