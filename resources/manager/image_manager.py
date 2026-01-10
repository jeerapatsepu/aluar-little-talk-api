import urllib

import cv2
import numpy as np

class ImageManager:
    def __init__(self, image_url: str):
        self.__image_url = image_url

    def verify_profile_photo(self):
        req = urllib.request.urlopen(self.__image_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        face = face_classifier.detectMultiScale(
            gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        return len(face) > 0