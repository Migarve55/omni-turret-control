

class Turret:
    def __init__(self):
        pass

    def connect_mqtt(self, port, broker):
        print("Connected to", port, broker)

    def disconnect_mqtt(self):
        print("Disconnected")

    def move(self, x, y):
        print(x, y)

    def shoot(self):
        print('BANG')