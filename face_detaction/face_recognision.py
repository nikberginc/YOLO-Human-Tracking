import cv2
from cv2_draw.cv2_ractangle import draw_rectangle
from YOLO.YOLO_human import YOLO_human
from orientation.routing import route



def face_algoritm(frame, org_width, org_height, number_of_frames, target):

    #program will make small frame for faster runing time
    small_frame = cv2.resize(frame, (300, 300))
    center_y = None
    center_x = None


    #program will get the human locations on the small frame version
    target = YOLO_human(small_frame, target)
#    target returns
#        target = {
#    "x1": x1,
#    "y1": y1,
#    "x2": x2,
#    "y2": y2,
#    "cx": cx,
#    "cy": cy,
#    "lost_frames": 0
#   }


    big_posision_list = []





    #if there are no humans program will return raw frame
    if target is None:
        return frame, big_posision_list, center_x, center_y, target
    
    #from target we distrackect all the nesesery cordinates and all necessary
    else:
        top = target["y1"]
        right = target["x2"]
        bottom = target["y2"]
        left = target["x1"]

        center_x = target["cx"]
        center_y = target["cy"]
    






    #program will get for how much shoud multiply the height and width of the image to get the ractangle in to the corect place on the picture
    x_scale = org_width / 300
    y_scale = org_height / 300

    #program will get the posisions of the ractangle on the normal image
    top = int(top * y_scale)
    right = int(right * x_scale)
    bottom = int(bottom * y_scale)
    left = int(left * x_scale)

    center_x = int(center_x * x_scale)
    center_y = int(center_y * y_scale)



    #program will store the posisions to one veriable
    coords = (top, right, bottom, left)
    #safety check so there are always 4 coordinats
    if len(coords) == 4:
        big_posision_list.append(coords)




    route(center_x, center_y, frame)


    #the program will draw ractengle on the human and than send the image back to the main program
    draw_rectangle(big_posision_list, frame, center_x, center_y)
    return frame, big_posision_list, center_x, center_y, target
    

   