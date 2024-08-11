import cv2
import time
import glob
from emailing import send_email
from emailing import clean_folder
from threading import Thread

x = 0
y = 0
w = 0
h = 0

def feed_monitor():
    global x
    global y
    global w
    global h
    first_frame = None
    status_list = []
    count = 1
    threaded_video = cv2.VideoCapture(0)
    time.sleep(5)

    while True:
        status = 0
        check, threaded_frame = threaded_video.read()

        gray_frame = cv2.cvtColor(threaded_frame, cv2.COLOR_BGR2GRAY)
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if first_frame is None:
            first_frame = gray_frame_gau

        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

        thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
        # cv2.imshow("My video", dil_frame)

        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(threaded_frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            if rectangle.any():
                status = 1
                cv2.imwrite(f"images/{count}.png", threaded_frame)
                count = count + 1
                all_images = glob.glob("images/*.png")
                index = int(len(all_images) / 2)
                image_with_object = all_images[index]


        
        status_list.append(status)
        status_list = status_list[-2:]

        if status_list[0] == 1 and status_list[1] == 0:
            email_thread = Thread(target=send_email, args=(image_with_object, ))
            email_thread.daemon = True
            email_thread.start()



feed_thread = Thread(target=feed_monitor)
feed_thread.daemon = True
feed_thread.start()

video = cv2.VideoCapture(0)
time.sleep(5)

while True:
    check, frame = video.read()
    rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    # print(status_list)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
try_cleaning = clean_folder()
while not try_cleaning:
    time.sleep(1)
    try_cleaning = clean_folder()