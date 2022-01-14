
from control.turret_stub import TurretStub
from control.turret import Turret
from vision.counter import MotionTracker
import cv2
from aiming.ballistics import *

broker = '192.168.1.5'
user = "production"
passwd = "trigliceridos"

counter = 0
threshold = 15

mouseX = 0
mouseY = 0
trigger = False


def auto_aim(tracker, turret, feed):
    global counter
    target = tracker.process_frame()
    if target is not None:
        (x, y, w, h) = target
        s_x = int(x + w / 2)
        s_y = int(y + h / 2)
        yaw = calculate_yaw(s_x)
        pitch = calculate_pitch(s_y)
        turret.move(yaw, pitch)
        draw_target(feed, s_x, s_y)
        counter += 1
        if counter > threshold:
            turret.shoot()
    else:
        counter = 0


def manual_aim(turret, feed):
    global mouseX, mouseY, trigger
    draw_target(feed, mouseX, mouseY)
    yaw = calculate_yaw(mouseX)
    pitch = calculate_pitch(mouseY)
    turret.move(yaw, pitch)
    if trigger:
        turret.shoot()


def draw_target(img, s_x, s_y):
    (img_height, img_width, _) = img.shape
    cv2.line(img, (0, s_y), (img_width, s_y), (0, 0, 200), 2)
    cv2.line(img, (s_x, 0), (s_x, img_height), (0, 0, 200), 2)
    cv2.circle(img, (s_x, s_y), 10, (0, 0, 200), 2)


def track_mouse(event, x, y, flags, param):
    global mouseX, mouseY, trigger
    mouseX = x
    mouseY = y
    trigger = event == cv2.EVENT_LBUTTONDOWN


def main():
    turret = TurretStub()
    tracker = MotionTracker()
    tracker.start()
    turret.connect_mqtt(broker, user, passwd)
    manual = True
    while True:
        feed = tracker.get_feed()
        key = cv2.waitKey(20)  # 50 fps
        # Modo
        if manual:
            manual_aim(turret, feed)
        else:
            auto_aim(tracker, turret, feed)
        # Interfaz
        mode = "Manual" if manual else "Auto"
        cv2.putText(feed, mode, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 1, cv2.LINE_AA)
        cv2.imshow("Feed", feed)
        cv2.setMouseCallback("Feed", track_mouse)
        # Teclado
        if key == ord('c'):
            manual = not manual
        if key == 27:
            break
    tracker.close()
    turret.disconnect_mqtt()


if __name__ == '__main__':
    main()
