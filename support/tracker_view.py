<<<<<<< HEAD
#!/usr/bin/env python
"Debugging tool for verifying the target tracking code with color masking."

# from lib import color_mask, util
import argparse
import cv2
from context import lib          # flake8: noqa pylint: disable=unused-import
from lib import color_mask, util, config, target_tracker

def run(channel, config_file):
    cfg = config.Config(filename=config_file)
    debug = cfg.get_default("debug", False)
    cr = cfg.get("color", "yellow")
    lower, upper = color_mask.unpack_range(cr)
    camera, width, height = util.get_video(channel)

    while True:
        hsv, img = util.get_hsv(camera)
        masked = color_mask.get_mask(hsv, lower, upper)
        res = cv2.bitwise_and(hsv, hsv, mask=masked)

        key = cv2.waitKey(1)

        if util.has_pressed(key, 'q'):
            break

        print(target_tracker.single_target(masked, img))
        cv2.imshow("image", img)
        cv2.imshow("res", res)
        # cv2.imshow("masked", masked)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-p', '--channel', default=1, type=int,
                        help ='the USB channel containing camera, 0, 1, or 2')
    PARSER.add_argument('-c', '--config',
                        help ='YAML filename that containing fudge factors and color calibration values')

    ARGS = PARSER.parse_args()

    print("""
    This program reads calibration and tracking fudge factors from the file:
    {0}

    It then displays multiple windows of the inside of what the tracking system
    sees through the USB camera attach to channel, {1}. Also prints the
    targeting information to the screen (note, these values will go to
    NetworkTables).

    Press 'q' to cancel and quit this application. *Note:* The keys must be
    pressed with the image window is the foremost window, otherwise, you can
    cancel this application with Control-C.
    """.format(ARGS.config, ARGS.channel))

    run(ARGS.channel, ARGS.config)
=======
#!/usr/bin/env python
"Debugging tool for verifying the target tracking code with color masking."

# from lib import color_mask, util
import argparse
import cv2
from context import lib          # flake8: noqa pylint: disable=unused-import
from lib import color_mask, util, config

DEBUG = True

def run(channel, config_file):
    cfg = config.Config(filename=config_file)
    DEBUG = cfg.get_default("debug", False)
    cr = cfg.get("color", "yellow")
    lower, upper = color_mask.unpack_range(cr)
    camera, width, height = util.get_video(channel)

    while True:
        hsv, img = util.get_hsv(camera)
        masked = color_mask.get_mask(hsv, lower, upper)
        res = cv2.bitwise_and(hsv, hsv, mask=masked)

        key = cv2.waitKey(1)

        if util.has_pressed(key, 'q'):
            break

        print(color_mask.single_target(masked, img))
        cv2.imshow("image", img)
        cv2.imshow("res", res)
        # cv2.imshow("masked", masked)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-p', '--channel', default=1, type=int,
                        help ='the USB channel containing camera, 0, 1, or 2')
    PARSER.add_argument('-c', '--config',
                        help ='YAML filename that containing fudge factors and color calibration values')

    ARGS = PARSER.parse_args()

    print("""
    This program reads calibration and tracking fudge factors from the file:
    {0}

    It then displays multiple windows of the inside of what the tracking system
    sees through the USB camera attach to channel, {1}. Also prints the
    targeting information to the screen (note, these values will go to
    NetworkTables).

    Press 'q' to cancel and quit this application. *Note:* The keys must be
    pressed with the image window is the foremost window, otherwise, you can
    cancel this application with Control-C.
    """.format(ARGS.config, ARGS.channel))

    run(ARGS.channel, ARGS.config)
>>>>>>> 3264d4e62bcd721e20fb13ac8aa2bb896698a379
