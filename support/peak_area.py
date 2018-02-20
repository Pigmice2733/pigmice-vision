"Demonstrates how to find maximum area associated with a peak on a curved graph."

import numpy as np
from context import lib  # flake8: noqa
from lib.rand import plot, random_bumpy_peak
from lib.math_extras import top_bell, max_peak_deviation


def demo():
    seq = random_bumpy_peak()

    print("Here is a curve where we have mapped the top peak.")
    begin, end = top_bell(seq)
    plot(seq, marks=[begin, end])

    print("Here is the standard deviation of the top peak.")
    lower_y, upper_y = max_peak_deviation(seq)
    plot(seq, marks=[lower_y, upper_y])

    print("Point associated with lower deviation:")
    lower_x = seq[lower_y]
    print(lower_x, lower_y)

    print("Point associated with max peak:")
    max_x = np.max(seq)
    max_y = np.argmax(seq)
    print(max_x, max_y)

    print("Point associated with upper deviation:")
    upper_x = seq[upper_y]
    print(upper_x, upper_y)


if __name__ == '__main__':
    """
    How can we get the index values of the standard deviation from a sequences
    maximum, but between two local mimimums?
    """
    demo()
