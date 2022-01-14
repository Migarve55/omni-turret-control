
from paho.mqtt import client as mqtt_client
import json

device = "SISTEM/master/torreta"


class Turret:
    def __init__(self):
        self.client = None
        self.connected = False

    def connect_mqtt(self, broker, user, passwd):
        client_id = 'python-controller'

        def on_connect(client, userdata, flags, rc):
            self.connected = rc == 0
        self.client = mqtt_client.Client(client_id)
        self.client.on_connect = on_connect
        self.client.username_pw_set(user, passwd)
        self.client.connect(broker)

    def disconnect_mqtt(self):
        self.client.disconnect()

    def move(self, x, y):
        command = {
                "command": "position",
                "arg1": int(y),
                "arg2": int(x)
            }
        self.send_command(command)

    def shoot(self):
        command = {"command": "dispara"}
        self.send_command(command)

    def send_command(self, command):
        msg = json.dumps(command)
        self.client.publish(device, msg)
