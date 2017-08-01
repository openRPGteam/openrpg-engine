import json
import draw
from main_field import Player, draw_battle, save_image
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


def check_battle(request):
    parsed = json.loads(request)
    if 'this' not in parsed.keys() or 'that' not in parsed.keys():
        return False, None
    if len(parsed["this"]) != 2 or len(parsed["that"]) != 2:
        return False, None
    l_pl, r_pl = parsed["this"], parsed["that"]
    if 'sprite' not in l_pl.keys() or 'sprite' not in r_pl.keys() or 'hp' not in r_pl.keys() or 'hp' not in l_pl.keys():
        return False, None
    if l_pl['sprite'] not in draw.BATTLE_TYPES[0].keys() or r_pl['sprite'] not in draw.BATTLE_TYPES[1].keys():
        return False, None
    if l_pl['hp'] not in range(101) or r_pl['hp'] not in range(101):
        return False, None
    else:
        p1 = Player(draw.BATTLE_TYPES[0][ l_pl['sprite'] ], l_pl['hp'])
        p2 = Player(draw.BATTLE_TYPES[1][ r_pl['sprite'] ], r_pl['hp'])
        return True, (p1, p2)


def process_battle(player_pair, path=""):
    bck = draw_battle(player_pair[0], player_pair[1])
    return save_image(bck, "{}{}.jpg".format(path, randint(10000000, 99999999)))