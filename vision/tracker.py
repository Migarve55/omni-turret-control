import cv2


def main():
    cam = cv2.VideoCapture(0)
    tracker = cv2.Tracker_()
    while True:
        (ok, frame) = cam.read()
        if not ok:
            break
        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        (ok, bbox) = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # Draw bounding box
        if ok:
            draw_target(frame, bbox)
        else:
            # Tracking failure
            print("Failed to detect")
        # Display tracker type on frame
        cv2.putText(frame, " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
        # Display result
        cv2.imshow("Tracking", frame)
        # Teclado
        key = cv2.waitKey(10)
        if key == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


def draw_target(img, box):
    (height, width, _) = img.shape
    (x, y, w, h) = box
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
    # Scope
    s_x = int(x + w / 2)
    s_y = int(y + h / 2)
    cv2.line(img, (0, s_y), (width, s_y), (0, 0, 200), 2)
    cv2.line(img, (s_x, 0), (s_x, height), (0, 0, 200), 2)
    cv2.circle(img, (s_x, s_y), 10, (0, 0, 200), 2)


if __name__ == '__main__':
    main()
