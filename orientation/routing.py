import cv2
#program will say where the human must go so it gets to the center(ractangle wich goes from top to bottom and has a small width,
#rectangle who goes from left to right and its small in hight and both are in the center)
def route(cx, cy, frame):


    #program will get the center of the frame
    h, w = frame.shape[:2]

    center_x = w // 2
    center_y = h // 2

    #program gets a stable width of the rectangle
    rect_width = w // 6
    rect_height = h // 6



    #program gets now all the cords for rectangle
    r_left = center_x - rect_width // 2
    r_right = center_x + rect_width // 2
    r_top = center_y - rect_height //2
    r_bottom = center_y + rect_height //2



    #program now sees if center of a human is needed to go RIGHT or LEFT or is already in CENTER
    if r_left <= cx <= r_right:
        print("\n\n\nCENTER   CENTER  CENTER  CENTER  CENTER  CENTER  CENTER  CENTER  CENTER")

    elif cx < r_left:
        print("\n\n\nRIGHT    RIGHT   RIGHT   RIGHT   RIGHT   RIGHT   RIGHT   RIGHT   RIGHT")

    elif cx > r_right:
        print("\n\n\nLEFT     LEFT    LEFT    LEFT    LEFT    LEFT    LEFT    LEFT    LEFT")


    #program now sees if center of a human is needed to go UP or DOWN or is already in CENTER
    if r_top <= cy <= r_bottom:
        print("CENTER   CENTER  CENTER  CENTER  CENTER  CENTER  CENTER  CENTER  CENTER")

    elif cy < r_top:
        print("DOWN    DOWN    DOWN    DOWN    DOWN    DOWN    DOWN    DOWN    DOWN")

    elif cy > r_bottom:
        print("UP       UP      UP      UP      UP      UP      UP      UP         UP")
