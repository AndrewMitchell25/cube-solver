import cv2
import numpy as np

def find_contours(frame2, frame):
    contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    final_contours = []
    # Filter for square contours
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
        area = cv2.contourArea(contour)
        (x, y, w, h) = cv2.boundingRect(approx)
        ratio = w / float(h)

        # Check if the contour is close to a square
        if ratio >= 0.8 and ratio <= 1.2 and w >= 30 and w <= 60 and area / (w*h) > 0.4:
            final_contours.append((x, y, w, h))
    if len(final_contours) < 9:
        return []
    

    # Find the center
    found = False
    contour_neighbors = {}
    for index, contour in enumerate(final_contours):
        (x, y, w, h) = contour
        contour_neighbors[index] = []
        center_x = x + w / 2
        center_y = y + h / 2
        radius = 1.5

        neighbor_positions = [
                # top left
                [(center_x - w * radius), (center_y - h * radius)],

                # top middle
                [center_x, (center_y - h * radius)],

                # top right
                [(center_x + w * radius), (center_y - h * radius)],

                # middle left
                [(center_x - w * radius), center_y],

                # center
                [center_x, center_y],

                # middle right
                [(center_x + w * radius), center_y],

                # bottom left
                [(center_x - w * radius), (center_y + h * radius)],

                # bottom middle
                [center_x, (center_y + h * radius)],

                # bottom right
                [(center_x + w * radius), (center_y + h * radius)],
            ]

        
        for neighbor in final_contours:
            (x2, y2, w2, h2) = neighbor
            for (x3, y3) in neighbor_positions:
                if (x2 < x3 and y2 < y3) and (x2 + w2 > x3 and y2 + h2 > y3):
                    contour_neighbors[index].append(neighbor)

    for (contour, neighbors) in contour_neighbors.items():
        if len(neighbors) == 9:
            found = True
            final_contours = neighbors
            break
    if not found:
        return []

    # Sort the contours
    y_sorted = sorted(final_contours, key=lambda x: x[1])

    top_sorted = sorted(y_sorted[0:3], key=lambda x: x[0])
    mid_sorted = sorted(y_sorted[3:6], key=lambda x: x[0])
    bot_sorted = sorted(y_sorted[6:9], key=lambda x: x[0])

    return top_sorted + mid_sorted + bot_sorted

def draw_contours(frame, contours):
    for index, (x, y, w, h) in enumerate(contours):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

sat_W = 60 
val_W = 150
orange_L = 8  
orange_H = 23  
yellow_H = 50  
green_H = 100  
blue_H = 160  

def get_colors(frame, contours):
    stickers = []
    for index, (x, y, w, h) in enumerate(contours):
        roi = frame[y+7:y+h-7, x+14:x+w-14]

        _, labels, palette = cv2.kmeans(np.float32(roi.reshape(-1, 3)), 1, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1), 10, cv2.KMEANS_RANDOM_CENTERS)
        _, counts = np.unique(labels, return_counts=True)
        h,s,v = palette[np.argmax(counts)]
        # print(h, s, v)
        if s <= sat_W and v >= val_W:
            stickers.append("U") # white
        elif orange_L <= h < orange_H:
            stickers.append("L") # orange
        elif orange_H <= h < yellow_H:
            stickers.append("D") # yellow
        elif yellow_H <= h < green_H:
            if s < 150:
                stickers.append("U") # white
            else:
                stickers.append("F") # green
        elif green_H <= h < blue_H:
            if s < 150:
                stickers.append("U") # white
            else:
                stickers.append("B") # blue
        else:
            stickers.append("R") # red

    return stickers[4], stickers

centers = {
    'U': 0,
    'R': 1,
    'F': 2,
    'D': 3,
    'L': 4,
    'B': 5,
}

def update_state_string(state_string, center, stickers):
    new_state = state_string[0:(centers[center]*9)] + "".join(stickers) + state_string[(centers[center]*9 + 9):]
    # print(new_state)
    return new_state


grid = {
    'white': [1, 0],
    'orange': [0, 1],
    'green': [1, 1],
    'red': [2, 1],
    'blue': [3, 1],
    'yellow': [1, 2],
}

colors = {
    'R'   : (0, 0, 255),
    'L': (0, 165, 255),
    'B'  : (255, 0, 0),
    'F' : (0, 255, 0),
    'U' : (255, 255, 255),
    'D': (0, 255, 255)
}

def draw_cube(width, height, frame, state_string):
    state_string = state_string[0:9] + state_string[36:45] + state_string[18:27] + state_string[9:18] + state_string[45:54] + state_string[27:36]

    tile_gap = 2
    tile_size = 14
    area_offset = 20

    side_offset = tile_gap * 3
    side_size = tile_size * 3 + tile_gap * 2

    offset_x = width - (side_size * 4) - (side_offset * 3) - area_offset
    offset_y = height - (side_size * 3) - (side_offset * 2) - area_offset

    for side_index, (side, (grid_x, grid_y)) in enumerate(grid.items()):
        index = -1
        for row in range(3):
            for col in range(3):
                index += 1
                x1 = ((offset_x + tile_size * col) + 
                        (tile_gap * col) +
                        ((side_size + side_offset) * grid_x))
                y1 = ((offset_y + tile_size * row ) + 
                        (tile_gap * row) +
                        ((side_size + side_offset) * grid_y))
                x2 = x1 + tile_size
                y2 = y1 + tile_size

                if state_string[side_index*9+index] != "0":
                    color = colors[state_string[side_index*9+index]]
                else:
                    color = (150, 150, 150)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), -1)
                cv2.rectangle(frame, (x1 + 1, y1 + 1), (x2 - 1, y2 - 1), color, -1)

solved_string = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
centers_string = "0000U00000000R00000000F00000000D00000000L00000000B0000"

def run():
    cap = cv2.VideoCapture(0)
    state_string = centers_string
    flag = 0
    while True:
        _, frame = cap.read()
        key = cv2.waitKey(1) & 0xff 
        if key == 27:
            state_string = -1
            break
        elif key == 13:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.blur(gray_frame, (3, 3))
        canny_frame = cv2.Canny(blurred_frame, 30, 60,3)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilated_frame = cv2.dilate(canny_frame, kernel)
        
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        contours = find_contours(frame, dilated_frame)
        #if len(contours) == 9 and flag == 0: 
        if len(contours) == 9: 
            draw_contours(frame, contours)
            center, stickers = get_colors(hsv, contours)
            state_string = update_state_string(state_string, center, stickers)
            flag = 1

        
        draw_cube(int(cap.get(3)), int(cap.get(4)), frame, state_string)
        cv2.imshow("Solver",frame)

    cap.release()
    cv2.destroyAllWindows() 
    return state_string

if __name__ == "__main__":
    run()