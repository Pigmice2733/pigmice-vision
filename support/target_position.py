""" Finds Center of objects, and then it's position of either left or right """
from context import lib
from lib.color_mask import load_range
import numpy as np
import time
import imutils #cv2 support functions
import cv2

def get_video():
    """
    Returns a camera frame. This should be called once at the
    beginning of your program, and the results are passed to
    most other functions in this module.
    """
    # initialize the camera and grab a reference to the raw camera capture
    camera = cv2.VideoCapture(1)
    # allow the camera to warmup
    time.sleep(0.1)

    # If you need to flip the camera view (camera needs to be upside down include
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    # frame = cv2.flip(frame,0)
    # out.write(frame)

    width = camera.get(3)
    height = camera.get(4)

    return camera, width, height


def release_camera():
    """
    Call once at the end of your program to release the camera
    back to the operating system.
    """
    # cleanup the camera and close any open windows
    camera.release()


def find_center(circle, frame):
    """
    Finds the center of the bounding box put around object
    """
    (x, y), radius = cv2.minEnclosingCircle(circle)
    M = cv2.moments(circle)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    mark_circle(circle, center, frame)

    return center, radius


def mark_circle(m, center, frame):
    """
    Puts a red dot in the center of the bounding box
    """
    x,y,w,h = cv2.boundingRect(m)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.circle(frame, center, 5, (0, 0, 255), -1)


def get_hsvimg(camera):
    # grab the current frame
    (grabbed, frame) = camera.read()

    frame = imutils.resize(frame, width=600)

    # convert to HSV color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    return hsv_img


def get_maskimg(hsv_img, lower, upper):
    thresh = cv2.inRange(hsv_img, lower, upper)

    # perform some clean up before contour operations
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    return thresh


def target_direction(masked_img, width):
    cnts = cv2.findContours(masked_img.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    # The largest one or two contours in the mask, then use
    # those to compute the centroid (center of an area):

    if len(cnts) > 0:
        c = sorted(cnts, key=cv2.contourArea)
        nradius = 0  # This will be reset later
        if len(cnts) == 1:
            ((mx, my), mradius) = find_center(c[-1], masked_img)
            cenx = mx
        else:
            ((mx, my), mradius) = find_center(c[-1], masked_img)
            ((nx, ny), nradius) = find_center(c[-2], masked_img)
            cenx = (nx + mx)/2
        cenf = width/2 # cenf = middle of the frame

        distance = cenf - cenx
        return ("Distance:", distance)
    else:
        return None


def get_colored_target(camera, lower, upper, width):
    hsvimg = get_hsvimg(camera)
    maskimg = get_maskimg(hsvimg, lower, upper)
    return target_direction(maskimg, width)


if __name__ == '__main__':  # If ran on terminal:
    get_colored_target()
