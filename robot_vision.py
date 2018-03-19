"""
The main file to call that takes vision tracking information and sends to
a network table.
Use `java -jar support/OutlineViewer-1.0.1.jar` in terminal to create a local
server, once you have everything installed (see README)
"""
from lib import config, tables, target_tracker, color_mask, util
import argparse

def run(cfg):
    # cfg is the list of values that contain channel, server, lower, and upper
    channel = cfg.get('channel')
    server = cfg.get('networktables')
    lu = cfg.get("color", "yellow")

    fudges = cfg.get_default("fudges", {"center_x": 0,
                                        "center_y": 0
                                        })

    lower, upper = color_mask.unpack_range(lu)

    camera, width, height = util.get_video(channel)

    debug = cfg.get_default("debug", False)
    tables.setup(server, printtoo = debug)

    while True:
        if debug:
            print("camera:", camera)
        hsv, _ = util.get_hsv(camera)
        if debug:
            print("hsv:", hsv)
        masked_img = color_mask.get_mask(hsv, lower, upper)
        target = target_tracker.single_target(masked_img)
        if debug:
            print("target:", target)
        send_target_data(target, fudges)
        update_fudges(tables, cfg)


def send_target_data(target, fudges):
    if target is not None:
        tables.send('center_x', target["center"]["x"] + fudges["center_x"])
        tables.send('center_y', target["center"]["y"] + fudges["center_y"])
        # tables.send('distance', target.distance)
        tables.send('orientation',target["orientation"])
        tables.send('size', target["size"])
        tables.send('height', target["height"])
        tables.send('width', target["width"])
        tables.send('xdir', target["xpos"][0])
        tables.send('xmag', target["xpos"][1])
        tables.send("ydir", target["ypos"][0])
        tables.send("ymag", target["ypos"][1])
    else:
        tables.send('center_x', 0)
        tables.send('center_y', 0)
        tables.send('orientation', "")
        tables.send('size', 0)
        tables.send('height', 0)
        tables.send('width', 0)
        tables.send('xdir', "")
        tables.send('xmag', 0)
        tables.send("ydir", "")
        tables.send("ymag", 0)

def update_fudges(tables, cfg):
    """
    Compare the values that may have been edited on the NetworkTables server
    with the current configuration values. If they are different,
    the configuration values are changed to the new values and saved in the
    configuration file.
    """
    x = tables.get_fudges("center_x")
    y = tables.get_fudges("center_y")
    if x != cfg.get("fudges", "center_x"):
        cfg.set("fudges", "center_x", x)
        cfg.save()
    if y != cfg.get("fudges", "center_y"):
        cfg.set("fudges", "center_y", y)
        cfg.save()

if __name__ == '__main__':
    # Able to add through the command line what config file to use, but the
    # pigmice-config.yaml is set as the default
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--config', help="Configuration filename")
    args = parser.parse_args()

    cfg = config.Config(args.config)  # from config file make an instance of the Config class
    run(cfg)
