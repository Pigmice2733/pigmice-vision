import cv2
import numpy as np
from graph import smooth
# Smooths data set so jagged edges don't become mins
from hist_math import max_peak_deviation
# Turns color values into bell curve and returns local mins
from take_image import take_img
# Takes and saves image


def take_image():
    image = take_img()
    cv2.imshow("image", image)


def color_hist(chan):
    """
    Splits the image into the three paths of hsv, so we can calculate each
    individual value's range
    """
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    color_frequency = [p[0] for p in hist]
    return np.array(color_frequency)
    # The numpy array (np.array) allows us to use these two demensional array


def image_colors(image):
    """
    After splitting the image into three channels of hsv it returns an array of
    all the color in image (call with image).
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Split into the three channels of hue, saturation, and value.
    # We then initialize a tuple of strings representing the colors.
    chans = cv2.split(hsv)

    return [color_hist(chan) for chan in chans]


def color_range(image):
    """
    Smooth values (from graph.py) and with max_peak_deviation finds the most
    frequent colors as a bell curve and returns the curve's local mins.
    Returns the lowest and highest values in an array.
    """
    min_color = []
    max_color = []

    for hist_channel in image_colors(image):
        l, u = max_peak_deviation(smooth(hist_channel))
        # The standard deviation creates too small of a range, about 50 is
        # needed to be added and subtracted from the min and max values to
        # account for changes in light
        min_color.append(l - 50)
        max_color.append(u + 50)

    lower = np.asarray(min_color) # Able to use two demensional array
    upper = np.asarray(max_color)

    return (lower, upper) # returns lowest and highest most frequent values


if __name__ == '__main__':
    # Takes an image to use
    take_image()
    # To hardcode an image to use:
    # image = cv2.imread("../support/samples/cube2.jpg")
