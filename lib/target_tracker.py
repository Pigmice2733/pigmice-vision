""" Finds Center of objects, and then it's position of either left or right """
import cv2
from lib import color_mask


def target_size(roi, img=[]):
    """
    Creates a circle around a given ROI (region of interest) to return
    the radius of the object.
    """
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
    """
    Describes if the object is to the right, left, or straight in the middle
    of the screen, this is the same for the y coordinates of up and down.
    This could be used to help the line the object in the center of the screen.
    """
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
    """
    Creates a bounding box (rectange) around a ROI and returns the height,
    width, and the orientation of the object (it's positioned horizontally
    or vertically).
    """
    x, y, width, height = cv2.boundingRect(roi)
    if len(img) > 0:
        cv2.rectangle(img, (x, y), (x+width, y+height), (255, 0, 0), 4)

    if width > height:
        orientation = "horizontal"
    else:
        orientation = "vertical"

    return height, width, orientation


def single_target(img, orig=[]):
    """
    Logic to find the center of a single target, such as a powercube.
    Returns center of object (x,y coordinate on image frame), size,
    and orientation of object.
    """

    contours = color_mask.get_contours(img)

    if len(contours) > 0:
        # ROI = region of interest, ie. largest contour (last in contours list)
        contour = contours[-1]
        roi = cv2.convexHull(contour)

        # Surround the contour shape in green:
        if len(orig) > 0:
            cv2.drawContours(orig, [roi], 0, (0, 255, 0), 4)

        size = target_size(roi, orig)
        width, height, orientation = height_width(roi, orig)
        center, xpos, x, ypos, y = offset_from_center(roi, img)

        return {
            'center': {'x': center[0], 'y': center[1]},
            'size': size,
            'height': height,
            'width': width,
            'orientation': orientation,
            'xpos': [xpos, x],
            "ypos": [ypos, y]
        }


def double_target(img):
    """
    Logic to find the center of two objects, such as two pieces of vision tape.
    Returns center of object (x,y coordinate on image frame), size,
    and orientation of object.
    """
    pass
