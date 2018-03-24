"""
The main file to call that takes vision tracking information and sends to
a network table.
Use `java -jar support/OutlineViewer-1.0.1.jar` in terminal to create a local
server, once you have everything installed (see README)
"""
from lib import config, tables, target_tracker, color_mask, util
from time import sleep
import argparse

# The `debug` global variable is a number that corresponds to how much
# debugging information we should attempt to print:
#   0 :: No output except for errors
#   1 :: Output only changes that may be of interest
#   2 :: Output all data sent to NetworkTables

debug = 1

# The `fudges` is a dictionary of offsets we use to help calibrate the
# target analysis based on the position of the camera and the _goal_ of
# the robot:

fudges = {"center_x": 0,
          "center_y": 0
          }


def debug_message(level, *msg):
    """
    A wee helper function for printing debugging messages if (and
    only if), the global variable, debug has been set...which should
    come from the configuration file.
    """
    global debug
    if debug >= level:
        print(*msg)


def run(cfg):
    """
    The primary code interface for the Vision Analysis program and the
    RoboRIO hosted NetworkTables.

    The configuration object, cfg, should have all the goodies on what
    to connect to, including the vision camera, the server hosting the
    NetworkTables, and the color range values.
    """
    # cfg is the list of values that contain channel, server, lower, and upper
    global debug
    debug = cfg.get_default("debug", 1)

    global fudges
    fudges["center_x"] = cfg.get_default("fudges", "center_x", 0)
    fudges["center_y"] = cfg.get_default("fudges", "center_y", 0)

    channel = cfg.get_default('channel', 0)
    server = cfg.get_default('networktables', '10.27.33.2')
    lu = cfg.get("color", "yellow")
    lower, upper = color_mask.unpack_range(lu)

    camera, width, height = util.get_video(channel)
    debug_message(1, "camera:", camera)

    if debug >= 2:
        tables.setup(server, printtoo=True)
    else:
        tables.setup(server)

    # We need to wait a bit for both the camera and the NetworkTables server
    # to "come online", so let's add a wee kludge and wait 5 seconds:
    sleep(5)

    # Send our fudgys and then put them into the NetworkTables, so that
    # we could change them if we want to.
    tables.send_fudge("center_x", fudges['center_x'])
    tables.send_fudge("center_y", fudges['center_y'])

    frame_width = width/2 # This is to calculate the offset in the next function

    while True:
        hsv, _ = util.get_hsv(camera)
        masked_img = color_mask.get_mask(hsv, lower, upper)
        target = target_tracker.single_target(masked_img)

        send_target_data(target, frame_width)
        update_fudges(tables, cfg)


def send_target_data(target, frame_width):
    """
    Send the target information over to the NetworkTables (using the `tables`
    interface) including any fudge factor offsets.
    """
    print(target)
    if target == None:
        tables.send('center_x', 0)
        tables.send('center_y', 0)
        tables.send('offset', 0)
    else:
        x = target["center"]["x"] + fudges["center_x"]
        y = target["center"]["y"] + fudges["center_y"]
        if abs(x) < 10:
            offset = 0
        else:
            offset = frame_width/x
        tables.send('center_x', x)
        tables.send('center_y', y)
        tables.send('offset', offset)


def update_fudges(tables, cfg):
    """
    Compare the values from the NetworkTables server (which we may change
    during calibration), and if they are different, persist them in our
    configuration file.
    """
    global fudges

    x = tables.get_fudge("center_x")
    y = tables.get_fudge("center_y")

    # If the fudge factor isn't in the NetworkTables, we will get a None value,
    # and should be ignored. However, if we get a value that is different than
    # what we have stored, let's update our fudgy values in our config:
    if x and x != fudges['center_x']:
        debug_message(1, "Changing `center_x` to ", x)
        fudges['center_x'] = x
        cfg.set("fudges", "center_x", x)
        cfg.save()

    if y and y != fudges['center_y']:
        debug_message(1, "Changing `center_y` to ", y)
        fudges['center_y'] = y
        cfg.set("fudges", "center_y", y)
        cfg.save()


if __name__ == '__main__':
    # Able to add through the command line what config file to use, but the
    # pigmice-config.yaml is set as the default
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--config', help="Configuration filename")
    args = parser.parse_args()

    # from config file make an instance of the Config class
    cfg = config.Config(args.config)

    run(cfg)
