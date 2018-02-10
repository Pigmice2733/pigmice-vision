import time
import cv2

def take_img(camera_port = 1):
    """Take an image and saves it to jpg (or override an image that already exists)"""
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)  # If you don't wait, the image will be dark
    return_value, img = camera.read()
    cv2.imwrite("../support/samples/cube1.jpg", img)
    del(camera)  # so that others can use the camera as soon as possible

    return img
