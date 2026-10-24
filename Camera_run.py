import cv2
from face_detaction.face_recognision import face_algoritm
from cv2_draw.cv2_ractangle import draw_rectangle
 
# Open the video file
cap = cv2.VideoCapture(0)
 
# Check if the camera was opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    print("Camera opened successfully!")
        

target = None
last_faces = []
frames_without_face = 0
big_face_list = []
number_of_frames = 1
# Read and display each frame of the video and using the function for face recognision
while True:
    
    #every frame will be stored in "frame" and be sent to the function
    ret, frame = cap.read()

    #ret is positive or negative, it shows if video become corupted or ended
    if not ret:
        print("End of video or error occurred.")
        break
 
    # Get original width and height
    org_height, org_width = frame.shape[:2]

    #program will do a ractangle on a face every N frames
    if number_of_frames % 5 == 0:
        #program will call the function and program will sort the list of locations of the faces in to its veriable and the procesed frame into the other
        frame, big_face_list, center_x, center_y, target = face_algoritm(frame, org_width, org_height, number_of_frames, target)

    
    
    

        #progrma will try to keep the ractangle on the face by just having the same posision prnted on the frame

        #program will check if big_face:list is empty/doesnt have 4 coords, if it is than it means the face wasnt on the camera at any point so it will skip the drawing line
        valid_faces = [coords for coords in big_face_list if len(coords) == 4]

        if valid_faces:
            cx = center_x
            cy = center_y
            last_faces = valid_faces
            frames_without_face = 0
            #draw_rectangle(valid_faces, processed_frame)
        else:
            frames_without_face += 1
    else:
        frames_without_face += 1
    


    # Draw rectangles if we have last_faces and frames_without_face < X frames
    if last_faces and frames_without_face < 30:
        draw_rectangle(last_faces, frame, cx, cy)

    cv2.imshow("Video Frame", frame)

    number_of_frames += 1
    #print (number_of_frames)





    #it will check every 1ms if a key was presssed
    key = cv2.waitKey(1) & 0xFF

    # Wait for 1ms for key press to continue or exit if 'q' is pressed
    if key == ord('q'):
        break
 
# Release the video capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()