import cv2
import numpy as np
from graph import smooth
from hist_math import max_peak_deviation
from rand import plot


def color_hist(chan):
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    color_frequency = [p[0] for p in hist]
    return np.array(color_frequency)


def image_colors(image):
    """
    After splitting the image into three channels of hsv it returns an array of
    all the color in image. Call with image.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Split the image into its three channels: hue, saturation, and value.
    # We then initialize a tuple of strings representing the colors.
    chans = cv2.split(hsv)

    return [color_hist(chan) for chan in chans]


def color_range(image):
    """
    Smooth values (from graph.py) and find the lowest and highest standard
    deviation (from hist_math.py). Returns the lowest and highest frequent hsv
    color values in a list.
    """
    lower = []
    upper = []

    for hist_channel in image_colors(image):
        #smooth(hist_channel))
        # Smooths data (from graph.py) and get color range
        l, u = max_peak_deviation(smooth(hist_channel))
        lower.append(l)
        upper.append(u)

    return (np.asarray(lower), np.asarray(upper))


if __name__ == '__main__':
    image = cv2.imread("../support/samples/cube1.jpg")
    cv2.imshow("image", image)
    cr = color_range(image)

    #print(cr)
