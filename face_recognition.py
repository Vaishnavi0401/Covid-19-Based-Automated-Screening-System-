import numpy as np
import cv2
import face_recognition as fr
from picamera import PiCamera

video_capture = cv2.VideoCapture(0)
#camera = PiCamera()
#camera.rotation = 180

vaishnavi_image= fr.load_image_file("/home/pi/Pictures/Images/Vaishnavi/vaishnavi.jpg")
vaishnavi_face_encoding = fr.face_encodings(vaishnavi_image)[0]

deeksha_image= fr.load_image_file("/home/pi/Pictures/Images/Deeksha/deeksha.jpg")
deeksha_face_encoding = fr.face_encodings(deeksha_image)[0]

tejas_image= fr.load_image_file("/home/pi/Pictures/Images/Tejas/tejas.jpg")
tejas_face_encoding = fr.face_encodings(tejas_image)[0]

apoorva_image= fr.load_image_file("/home/pi/Pictures/Images/Apoorva/apoorva.jpg")
apoorva_face_encoding = fr.face_encodings(apoorva_image)[0]

meghana_image= fr.load_image_file("/home/pi/Pictures/Images/Meghana/meghana.jpg")
meghana_face_encoding = fr.face_encodings(meghana_image)[0]







known_face_encoding = [vaishnavi_face_encoding,deeksha_face_encoding,tejas_face_encoding,apoorva_face_encoding,meghana_face_encoding]
known_face_names = ["Vaishnavi","Deeksha","Tejas","Apoorva","Meghana"]


while True:
    check,frames = video_capture.read()

    face_locations = fr.face_locations(frames)
    face_encodings = fr.face_encodings(frames,face_locations)

    for (top,right,bottom,left),face_encodings in zip(face_locations,face_encodings):

        matches = fr.compare_faces(known_face_encoding,face_encodings)

        name = "Unknown"

        face_distance = fr.face_distance(known_face_encoding,face_encodings)

        best_match_index = np.argmin(face_distance)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        cv2.rectangle(frames,(left,top),(right,bottom),(0,255,0),3)

        cv2.rectangle(frames,(left,bottom -35),(right,bottom),(0,255,0),cv2.FILLED)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frames,name,(left,bottom - 6),font,1.0,(255,255,255),1)

    resized = cv2.resize(frames,(500,500))
    cv2.imshow("Face Recognition",resized)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()


