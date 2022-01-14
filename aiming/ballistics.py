
import math

width = 640
height = 480

min_yaw = 0
max_yaw = 180
offset_yaw = 90

min_pitch = 30
max_pitch = 60
offset_pitch = 90

distance = 200  # in cm
field_width = 100  # in cm
cm_per_pixel = field_width / width


def calculate_yaw(x):
    deg = get_angle_degrees(x, width)
    return get_turret_degrees(deg, offset_yaw, min_yaw, max_yaw)


def calculate_pitch(y):
    deg = get_angle_degrees(y, height)
    return get_turret_degrees(deg, offset_pitch, min_pitch, max_pitch)


def get_angle_degrees(pixels, length):
    val = pixels - length / 2
    cm = val * cm_per_pixel
    rads = math.atan(cm / distance)
    return math.degrees(rads)


def get_turret_degrees(degrees, offset, min_degrees, max_degrees):
    return max(min(degrees, max_degrees), min_degrees) + offset


if __name__ == '__main__':
    while True:
        c = int(input("Val: "))
        print(get_angle_degrees(c, 100))
