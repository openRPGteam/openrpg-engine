import json
import draw
from random import randint


def check_request(json_req):
    parsed = json.loads(json_req)
    if 'cells_per_axle' not in parsed.keys() or 'array' not in parsed.keys():
        return False, None
    if len(parsed['array']) != parsed['cells_per_axle'] ** 2:
        return False, None
    return True, parsed


def extract_request(req, path=""):
    drawer = draw.draw(req['cells_per_axle'], 50)
    arr = req['array']
    for pos in range(req['cells_per_axle'] ** 2):
        res = drawer.set_cell(pos, arr[pos]['terrain_type'])
        if len(arr[pos]) == 2:
            res = drawer.draw_transparent(pos, arr[pos]["player"])
        if res == False:
            return "error"
    drawer.add_markup(req['cells_per_axle'])
    return drawer.save_image(path + '{}.jpg'.format(randint(10000000, 99999999))).split('/')[-1]
