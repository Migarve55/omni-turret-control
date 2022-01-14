

class TurretStub:
    def __init__(self):
        pass

    def connect_mqtt(self, broker, user, passwd):
        print("Connected to: ", broker)

    def disconnect_mqtt(self):
        print("Disconnected")

    def move(self, yaw, pitch):
        print(f'Yaw: {yaw}º, Pitch: {pitch}º')

    def shoot(self):
        print('BANG')