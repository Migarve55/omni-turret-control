
width = 640
height = 480

min_yaw = 0
max_yaw = 180

min_pitch = 30
max_pitch = 60


def calculate_yaw(x):
    return linear_map(x, 0, width, min_yaw, max_yaw)


def calculate_pitch(y):
    return linear_map(y, 0, height, min_pitch, max_pitch)


def linear_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
