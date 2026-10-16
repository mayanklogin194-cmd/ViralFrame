import cv2
import numpy as np

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def enhance_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]

        face = cv2.detailEnhance(face, sigma_s=10, sigma_r=0.15)

        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        face = cv2.filter2D(face, -1, kernel)

        image[y:y+h, x:x+w] = face

    return image
