import render
from random import randint

def in_vision_field(pos1, pos2):
    """find out if the distance between two characters is small enough"""
    return abs(pos1[0] - pos2[0]) < 218 and abs(pos2[1] - pos1[1]) < 218

def pos_in_vfield(mover1, mover2):
    """convert position on general map to image position"""
    p1, p2 = mover1.user.get_pos(), mover2.user.get_pos()
    return (177 - (p1[0] - p2[0]), 177 - (p1[1] - p2[1]))


class character:
    # TODO: remove default map_pos argument, no randomness in such way
    def __init__(self, sprite_file, map_pos=[42 * randint(10, 60), 42 * randint(10, 35)]):
        self.sprite = sprite_file
        self.map_pos = map_pos

    def getstrpos(self):
        """position for filename"""
        return str(self.map_pos[0]) + str(self.map_pos[1])

    def get_pos(self):
        """position on map getter"""
        return self.map_pos


class mover:
    user = 0

    def __init__(self, user):
        self.user = user

    def spawn(self):
        return render.draw_map(self.user.map_pos, self.user.sprite)

    def left(self):
        self.user.map_pos[0] -= 42
        return self.spawn()

    def right(self):
        self.user.map_pos[0] += 42
        return self.spawn()

    def up(self):
        self.user.map_pos[1] -= 42
        return self.spawn()

    def down(self):
        self.user.map_pos[1] += 42
        return self.spawn()


def save_background(image, filename, quality=80):
    image.save(filename, "JPEG", optimize=True, quality=quality)
    image.close()
    return filename