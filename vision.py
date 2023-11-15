import cv2 as cv2
import numpy as np

colors = {
    "red": [(0, 150, 170), (10, 255, 255)],
    "orange": [(10, 150, 125), (20, 255, 255)],
    "yellow": [(21, 120, 125), (45, 255, 255)],
    "green": [(50, 100, 100), (100, 255, 255)],
    "blue": [(101, 150, 125), (120, 255, 255)],
    "white": [(75, 0, 125), (125, 50, 255)]
}

colors_og = {
    "red": [(161, 75, 75), (255, 255, 255)],
    "red2": [(0, 75, 75), (10, 255, 255)],
    "orange": [(10, 100, 100), (23, 255, 255)],
    "yellow": [(24, 100, 100), (50, 255, 255)],
    "green": [(51, 100, 100), (100, 255, 255)],
    "blue": [(101, 100, 100), (160, 255, 255)],
    "white": [(75, 0, 99), (179, 62, 255)]
}

rect_colors = {
    "red": (0, 0, 255),
    #"red2": (0, 0, 255),
    "orange": (0, 110, 255),
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "white": (255, 255, 255),
}

def detect_color(lower_range, upper_range, frame, hsv, rect_color):
    #open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    #close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    mask=cv2.inRange(hsv,lower_range,upper_range)
    #mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel, iterations=1)
    #mask=cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=5)
    #mask=cv2.merge([mask, mask, mask])
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    #res = []

    for c in cnts:
        min_size=600
        max_size=1200
        if cv2.contourArea(c)>min_size and cv2.contourArea(c)<max_size:
            x,y,w,h=cv2.boundingRect(c)
            center_x = int(x+x+w)//2
            center_y = int(y+y+h)//2
            cv2.circle(frame, (center_x,center_y), 4, (255, 0, 255), -1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),rect_color,2)
            #res.append(c)
    #return res
    


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ret, frame = cap.read()
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #contours = []
        for color in colors:
            cs = detect_color(colors[color][0], colors[color][1], frame, hsv, rect_colors[color])        
            #contours += cs
        cv2.imshow("FRAME",frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows() 