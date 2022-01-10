
from paho.mqtt import client as mqtt_client


class Turret:
    def __init__(self):
        self.client = None
        self.connected = False

    def connect_mqtt(self, port, broker):
        client_id = 'python-controller'

        def on_connect(client, userdata, flags, rc):
            self.connected = rc == 0
        self.client = mqtt_client.Client(client_id)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)

    def disconnect_mqtt(self):
        self.client.disconnect()

    def move(self, x, y):
        msg = '{"command":"position","arg1":' + int(y) + ',"arg2":' + int(x) + '}'
        self.client.publish("SISTEM/master/torreta", msg)

    def shoot(self):
        msg = '{"command":"dispara"}'
        self.client.publish("SISTEM/master/torreta", msg)
