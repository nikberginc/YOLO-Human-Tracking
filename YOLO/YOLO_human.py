from ultralytics import YOLO
import cv2

#program will load up the needed modules
net = YOLO("modules/yolov8n.pt")


def YOLO_human(frame, target, confidence_threshold=0.5):

    old_target = target
    center_x = None
    center_y = None
    best_distance = float("inf")
    threshold = 10000
    best_score = float("inf")

    #it will get the detaction of human
    results = net(frame)




    #program goes and finds all results YOLO had found
    for r in results:


        #progrma goes trhoue every description of every results
        for box in r.boxes:

            #program checks if the class id is human
            clas = int(box.cls[0])
            #program checks what confidence YOLO has that it is the correct class
            conf = float(box.conf[0])


            #program procedes if confidence is more than confidence_threshold and class is 0
            if clas == 0 and conf > confidence_threshold:


                #program gets the posision from the box(basicly a description of resoult)
                x1, y1, x2, y2  = map(int, box.xyxy[0])








                #if target is None it means that program shoud pick the person closest to the middle of the screen
                if old_target is None:



                    #program gets the center of the frame
                    h, w = frame.shape[:2]
                    center_x = w // 2
                    center_y = h // 2


                    #program gets the center of a person
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2


                    #program calculate the distance of the center of a person to the center of the frame
                    dx = cx - center_x
                    dy = cy - center_y
                    distance = dx*dx + dy*dy


                    #program gets the closest person top the center
                    if distance < best_distance:

                        best_distance = distance


                        target = {
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2,
                            "cx": cx,
                            "cy": cy,
                            "lost_frames": 0
                        }



                #if target is not None it means the program will try to track the same humam, by compering the center of previus frame to new frame.
                else:
                    


                    #we get the old center posisions of the frame with the human.
                    old_cx = old_target["cx"]
                    old_cy = old_target["cy"]



                    #program gets the center of a human on this new frame
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    
                   


                    #program now calculates with the formula the distane betwen the two centers
                    dx = cx - old_cx
                    dy = cy - old_cy
                    score = dx*dx + dy*dy


                    #if score is valid it will continue
                    if score < threshold:


                        #if score is less than before, the scores cordinates will be set for target
                        if score < best_score:
                            best_score = score
                            target = {
                                "x1": x1,
                                "y1": y1,
                                "x2": x2,
                                "y2": y2,
                                "cx": cx,
                                "cy": cy,
                                "lost_frames": 0
                        }
                            
                  
    # CASE 1: there was no old target before
    # program was only trying to find a new person closest to the screen center
    if old_target is None:
        return target


    # CASE 2: there WAS an old target before
    #program found a good enough new match, return it
    if target is not None and best_score < threshold:
        return target


    # CASE 3: there was an old target, but it did NOT find a good enough match
    # so increase lost_frames on the OLD target
    old_target["lost_frames"] += 1

    if old_target["lost_frames"] >= 5:
        return None

    return old_target