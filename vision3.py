import cv2 as cv2
import numpy as np

colors = {
    "red": [(161, 128, 128), (255, 255, 255)],
    "orange": [(6, 128, 128), (23, 255, 255)],
    "yellow": [(24, 128, 128), (50, 255, 255)],
    "green": [(51, 128, 128), (100, 255, 255)],
    "blue": [(101, 128, 128), (160, 255, 255)],
    "white": [(75, 0, 99), (179, 62, 255)]
}

rect_colors = {
    "red": (255, 0, 0),
    "orange": (255, 110, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
}

def detect_color(lower_range, upper_range, frame, hsv, rect_color):
    mask=cv2.inRange(hsv,lower_range,upper_range)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x:
            x,y,w,h=cv2.boundingRect(c)
            center_x = int(x+x+w)//2
            center_y = int(y+y+h)//2
            cv2.circle(frame, (center_x,center_y), 4, (255, 0, 255), -1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),rect_color,2)
            # cv2.putText(frame,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, frame = cap.read()
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        for color in colors:
            detect_color(colors[color][0], colors[color][1], frame, hsv, rect_colors[color])
        cv2.imshow("FRAME",frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows() 