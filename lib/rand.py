import numpy as np
import math
import matplotlib.pyplot as plt


def plot(ary, label="Frequency", marks=[]):
    """
    Simple function to visually display an array of numbers.

    The marks is an array of `y` values that will be highlighted with a
    vertical bar.
    """
    plt.plot(ary)
    plt.ylabel(label)
    if len(marks) > 0:
        for m in marks:
            plt.axvline(x=m)
    plt.show()


# First, I need some random values to play with, and it would be nice to have
# these be /clustered/ such that if I graphed them in order, I would end up
# with a bell curve, for instance:
#
#     v = np.random.normal(size=10)

# Which could look like:
#
# [ 0.20085976  1.77831171 -0.70151459 -0.19543572  1.03648566
#  -0.33527645  0.02794574 -0.83083124  0.18109586 -0.63390043]
#
# We can figure out the lowest and largest value:
#
#     np.max(v)   => 1.77831171288044
#     np.min(v)   => -0.8308312386241851
#
# However, for my purposes, I really want everything to be a positive number,
# so I want to /shift/ all numbers up so that the lowest number is 0. While
# this no longer is a normal distribution, I'm fine with this for my
# experiments.
#
# So we created the `shift_to_zero` function. Notice that since the minimum
# value is /probably/ a negative value, I add its absolute value, in order to
# /increase/ the number to at least 0, which results in transforming our array
# like:
#
#     [1.031691   2.60914295 0.12931664 0.63539552 1.8673169
#      0.49555478 0.85877698 0.         1.0119271  0.19693081]

def shift_to_zero(ary):
    """
    Adds a number to every value in the given array such that the
    lowest number is 0, and all other numbers are greater than that.
    """
    lowest = np.min(ary)
    increase = np.vectorize(lambda n: n + abs(lowest))
    return increase(ary)


# I'd like to have my numbers in a range from 0 to 100, which means I need to
# /scale/ the values by some number. Since I don't feel the need to have
# /exactly/ 100, perhaps I could round the largest value to some integer, and
# then get a factor dividing by 100, so we wrote `scale_to_100`.
#
# Suppose my largest number was 2.2, I would like to /round up/ to 3, and use
# that value to divide by 100 in order to calculate the scaling factor, so I
# use the =ceil= function from the =math= library.
#
# Calling both functions on my array gives me:
#
#     scale_to_100( shift_to_zero(v) )
#
# Returns:
#
#  [34.3897     86.97143172  4.3105548  21.17985059 62.24389663
#   16.51849283 28.62589921  0.         33.73090324  6.56436021]

def scale_to_100(ary):
    """
    Multiplies every element in the array given by a number that
    will scale all numbers _close to_, but not greater than 100.
    """
    highest = np.max(ary)
    factor = 100 / math.ceil(highest)
    scale = np.vectorize(lambda n: n * factor)
    return scale(ary)


# However, in order to mimic the histogram plots we've been generating, we may
# need /order/ them such that the largest is somewhere in the middle, and that
# it tapers down on both ends. Something like the following function should
# suffice:

def bell_sort(ary):
    """
    Sorts an array where the largest value is in moved to the
    middle of the array, and the lowest values are towards the
    first and end of the array. For an array of linear values,
    this would result in a triangular looking array, however,
    with a normal distribution, this should resemble a
    standard bell curve.
    """
    mid = ary.size // 2

    # Sort changes the array, and doesn't return the new sorted array,
    # so we to create two new arrays, first and second halves:
    f_half = ary[0:mid]
    s_half = ary[mid:]
    f_half.sort()
    s_half.sort()

    # Combine the two arrays with append, but reverse the order
    # of the second half with the flip function:
    return np.append(f_half, np.flip(s_half, axis=-1))


# Finally, we wrap all this in a function we can now use to investigate random
# bell curve arrays, `random_bell`:

def random_bell(size=10):
    """
    Generate a array of random numbers of the size given, but
    order the numbers along a bell curve with values ranging
    from 0 up to 100.
    """
    v = np.random.normal(size=size)
    nums = scale_to_100(shift_to_zero(v))
    return bell_sort(nums).astype(int)


# While the `random_bell` generator will be nice under certain simplistic
# circumstances, if we want to play around with a more histogram-like curve, we
# can use a sophisticated function that permutes a single line into a wavy
# curve with a maximum.

def random_bumpy_peak(size=1000):
    """
    Generates an array of random numbers with a single maximum peak (near the
    center), and a number of lower peaks and valleys, with more closely
    resembles a single channel from a color histogram. Look for multiple
    maximums and minimums.
    """
    x = np.linspace(0, 4, size)  # Generates a straight line of data points
    return .2*np.sin(10*x) + np.exp(-abs(2-x)**2)
