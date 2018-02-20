""" Finds Center of objects, and then it's position of either left or right """
import cv2


def target_size(roi, img=[]):
    (x, y), radius = cv2.minEnclosingCircle(roi)
    radius = round(radius)
    if len(img) > 0:
        cv2.circle(img, (int(x), int(y)), radius, (255, 0, 0), 8)
    return radius


def find_contour_center(contour):
    """
    Given a contoured shape, return the center of the shape in x and y value.
    This is based on the weight and distribution of pixels,
    rather than the shape itself.
    """
    # M is image moments, this dictionary helps calculate features like center
    # of mass of the object, area of the object etc.
    M = cv2.moments(contour)
    # Calculate the centroid (center of target) as x and y coordinates
    # Reference: https://is.gd/mp58uU
    try:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx, cy

    except ZeroDivisionError:
        return (0, 0)


def offset_from_center(roi, img):
    cx, cy = find_contour_center(roi)
    center = (cx, cy)
    cv2.circle(img, (cx, cy), 3, (0, 0, 255), 3)
    # The first two values of frame perameters (height and width)
    fh, fw = img.shape[:2]
    x = -fw/2+cx
    if x < 0:
        xpos = "left"
    elif x > 0:
        xpos = "right"
    else:
        xpos = "straight"

    y = -fh/2+cy
    if y < 0:
        ypos = "up"
    elif y > 0:
        ypos = "down"
    else:
        ypos = "straight"

    return center, xpos, x, ypos, y


def height_width(roi, img=[]):
    x, y, width, height = cv2.boundingRect(roi)
    if len(img) > 0:
        cv2.rectangle(img, (x, y), (x+width, y+height), (255, 0, 0), 4)

    if width > height:
        orientation = "horizontal"
    else:
        orientation = "vertical"

    return height, width, orientation
