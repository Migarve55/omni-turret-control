import cv2


def main():
    cam = cv2.VideoCapture(0)
    # Lee la referencia
    t_minus = read_frame(cam)
    t = read_frame(cam)
    t_plus = read_frame(cam)
    while True:
        delta = diff_img(t_minus, t, t_plus)
        threshold = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)
        (shapes, _) = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Filtrado
        max_area = 0
        target = None
        for s in shapes:
            area = cv2.contourArea(s)
            if area < 800:
                continue
            if area > max_area:
                max_area = area
                target = s
        # Interfaz
        (_, img) = cam.read()
        if target is not None:
            draw_target(img, target)
        cv2.imshow("Camera", img)
        key = cv2.waitKey(10)
        # Releer
        t_minus = t
        t = t_plus
        t_plus = read_frame(cam)
        # Teclado
        if key == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


def read_frame(cam):
    (_, frame) = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (21, 21), 0)


def diff_img(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def draw_target(img, shape):
    (height, width, _) = img.shape
    (x, y, w, h) = cv2.boundingRect(shape)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
    # Scope
    s_x = int(x + w / 2)
    s_y = int(y + h / 2)
    cv2.line(img, (0, s_y), (width, s_y), (0, 0, 200), 2)
    cv2.line(img, (s_x, 0), (s_x, height), (0, 0, 200), 2)
    cv2.circle(img, (s_x, s_y), 10, (0, 0, 200), 2)


if __name__ == '__main__':
    main()
