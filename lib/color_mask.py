import cv2
import numpy as np
from color_range import color_range, take_image
import sys

def get_frame(cap, scaling_factor):
    """
    Captures the input frame from webcam
    """
    ret, frame = cap.read()
    # Resize the input frame
    frame = cv2.resize(frame, None, fx=scaling_factor,
                        fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return frame


def run_mask():
    """
    Only displays colors in a determined range of the most frequent colors in video feed
    """
    cap = cv2.VideoCapture(1)
    # Video Capture from input 1 (external usb camera), input 0 (built in camera)
    scaling_factor = 0.5
    lower = np.asarray([0,0,0]) # Start by showing all colors until image is inputted
    upper = np.asarray([255,255,255])

    while True:
        # Check if the user pressed ESC key
        c = cv2.waitKey(5)
        if c == 27:
            break

        frame = get_frame(cap, scaling_factor)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert the HSV colorspace

        if c == ord("c"):
            # If "c" is pressed recall color_range function to mask again
            lower, upper = color_range(hsv)
            print("lower", lower, "upper", upper)

        mask = cv2.inRange(hsv, lower, upper)
        # mask image using the range of colors given from the color_range function

        res = cv2.bitwise_and(frame, frame, mask=mask)
        res = cv2.medianBlur(res, 5)

        cv2.imshow('Original image', frame) # Show the orginal image
        cv2.imshow("Mask", mask) # Show the object you are masking in black and white
        cv2.imshow('Color Detector', res) # Show image with completed mask

    cv2.destroyAllWindows()

if __name__=='__main__': # If ran on terminal:
    run_mask()
