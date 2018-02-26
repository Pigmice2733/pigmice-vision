"""
The main file to call that takes vision tracking information and sends to
a network table.
Use `java -jar support/OutlineViewer-1.0.1.jar` in terminal to create a local
server, once you have everything installed (see README)
"""
from lib import config, tables, target_tracker, color_mask, util

def run(cfg):
    channel = cfg.get('channel')
    server = cfg.get('networktables')
    lu = cfg.get("color", "yellow")
    lower, upper = color_mask.unpack_range(lu)
    camera, width, height = util.get_video(channel)
    DEBUG = cfg.get_default("debug", False)
    tables.setup(server, printtoo = DEBUG)

    while True:
        if DEBUG:
            print("camera:", camera)
        hsv, _ = util.get_hsv(camera)
        if DEBUG:
            print("hsv:", hsv)
        masked_img = color_mask.get_mask(hsv, lower, upper)
        target = color_mask.single_target(masked_img)
        if DEBUG:
            print("target:", target)
        send_target_data(target)


def send_target_data(target):
    if target is not None:
        tables.send('center_x', target["center"]["x"])
        tables.send('center_y', target["center"]["y"])
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
        # tables.send('distance', 0)
        tables.send('orientation', "")
        tables.send('size', 0)
        tables.send('height', 0)
        tables.send('width', 0)
        tables.send('xdir', "")
        tables.send('xmag', 0)
        tables.send("ydir", "")
        tables.send("ymag", 0)

if __name__ == '__main__':
    cfg = config.Config() # from config file make an instance of the Config class
    run(cfg)
