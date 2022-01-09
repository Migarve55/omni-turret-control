import cv2


class MotionTracker:
    def __init__(self):
        self.cam = None
        self.ref = None
        self.counter = 0
        self.limit = 10

    def start(self):
        self.cam = cv2.VideoCapture(0)
        self.ref = self.read_frame()

    def process_frame(self):
        frame = self.read_frame()
        delta = cv2.absdiff(self.ref, frame)
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
                target = cv2.boundingRect(s)
        # Releer
        self.counter += 1
        if self.counter > self.limit:
            self.counter = 0
            self.ref = self.read_frame()
        # Devolver las coordenadas
        return target

    def close(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def get_feed(self):
        (_, frame) = self.cam.read()
        return frame

    def read_frame(self):
        (_, frame) = self.cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(gray, (21, 21), 0)


def draw_target(img, shape):
    (height, width, _) = img.shape
    (x, y, w, h) = shape
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
    # Scope
    s_x = int(x + w / 2)
    s_y = int(y + h / 2)
    cv2.line(img, (0, s_y), (width, s_y), (0, 0, 200), 2)
    cv2.line(img, (s_x, 0), (s_x, height), (0, 0, 200), 2)
    cv2.circle(img, (s_x, s_y), 10, (0, 0, 200), 2)


if __name__ == '__main__':
    detector = MotionTracker()
    detector.start()
    while True:
        t = detector.process_frame()
        # Interfaz
        feed = detector.get_feed()
        if t is not None:
            draw_target(feed, t)
        cv2.imshow("Camera", feed)
        if cv2.waitKey(10) == 27:
            break
    detector.close()
