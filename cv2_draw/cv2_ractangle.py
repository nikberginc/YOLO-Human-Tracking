import cv2


def draw_rectangle(big_posision_list, frame, center_x = None, center_y = None):

    #the program will draw all ractengles on the face and than send the image back to the main program
    for (top1, right1, bottom1, left1) in big_posision_list:
        cv2.rectangle(frame, (left1, top1), (right1, bottom1), (0, 255, 0), 2)
    
    #if there are cordinates for a circle at the middle of the human, the program will do it.
    if center_x is not None:
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)



    