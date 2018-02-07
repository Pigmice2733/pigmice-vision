import cv2
import numpy as np
from color_range import color_range
import sys


# Capture the input frame from webcam
def get_frame(cap, scaling_factor):
    # Capture the frame from video capture object
    ret, frame = cap.read()

    # Resize the input frame
    frame = cv2.resize(frame, None, fx=scaling_factor,
                       fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return frame


def run_mask():
    cap = cv2.VideoCapture(0)
    scaling_factor = 0.5
    lower = np.asarray([0,0,0])
    upper = np.asarray([250,250,250])

    # Iterate until the user presses ESC key
    while True:
        # Check if the user pressed ESC key
        c = cv2.waitKey(5)
        if c == 27:
            break

        frame = get_frame(cap, scaling_factor)
        # hsv_max = color_range.hsv_max(frame)
        # Convert the HSV colorspace
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define 'blue' range in HSV colorspace
        # lower = np.array([60,100,100])
        # upper = np.array([180,255,255])
        if c == ord("c"):
            lower, upper = color_range(hsv)
            print("lower", lower, "upper", upper)

        mask = cv2.inRange(hsv, lower, upper)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        res = cv2.medianBlur(res, 5)

        cv2.imshow('Original image', frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Lower Color", lower)
        cv2.imshow("Upper Color", upper)
        cv2.imshow('Color Detector', res)



    cv2.destroyAllWindows()

if __name__=='__main__':
    run_mask()
