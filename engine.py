import render

class character:
    def __init__(self, sprite_file, map_pos=[1500, 850], user_pos=[150,150]):
        self.sprite = sprite_file
        self.map_pos = map_pos
        self.user_pos = user_pos
        backg = render.get_background(map_pos, 400)
        backg = render.fill_with_shit(backg)
        self.background = backg
    # needed for pseudo-unique filename in engine-test-bot.py
    def getpos(self):
        return self.user_pos[0] + self.user_pos[1]
class mover:
    user = 0
    def __init__(self, user):
        self.user = user

    def spawn(self):
        # add user sprite to the background
        background = render.add_dynamic_sprites(self.user.background.copy(), (self.user.sprite, tuple(self.user.user_pos)))
        return background

    def left(self):
        if self.user.user_pos[0] >= 20:
            self.user.user_pos[0] -= 20
            background = render.add_dynamic_sprites(self.user.background.copy(), (self.user.sprite, tuple(self.user.user_pos)))
        else:   # if space left on map isn`t enough, move the map
            self.user.map_pos[0] -= 400
            background = render.get_background(self.user.map_pos, 400)
            self.user.user_pos[0] = 370
            background = render.fill_with_shit(background)
            self.user.background = background.copy()
            background = render.add_dynamic_sprites(background, (self.user.sprite, tuple(self.user.user_pos)))
        return background

    def right(self):
        if self.user.user_pos[0] <= 350:
            self.user.user_pos[0] += 20
            background = render.add_dynamic_sprites(self.user.background.copy(), (self.user.sprite, tuple(self.user.user_pos)))
        else:
            self.user.map_pos[0] += 400
            background = render.get_background(self.user.map_pos, 400)
            self.user.user_pos[0] = 0
            background = render.fill_with_shit(background)
            self.user.background = background.copy()
            background = render.add_dynamic_sprites(background, (self.user.sprite, tuple(self.user.user_pos)))
        return background

    def up(self):
        if self.user.user_pos[1] >= 20:
            self.user.user_pos[1] -= 20
            background = render.add_dynamic_sprites(self.user.background.copy(), (self.user.sprite, tuple(self.user.user_pos)))
        else:
            self.user.map_pos[1] -= 400
            background = render.get_background(self.user.map_pos, 400)
            self.user.user_pos[1] = 340
            background = render.fill_with_shit(background)
            self.user.background = background.copy()
            background = render.add_dynamic_sprites(background, (self.user.sprite, tuple(self.user.user_pos)))
        return background

    def down(self):
        if self.user.user_pos[1] <= 320:
            self.user.user_pos[1] += 20
            background = render.add_dynamic_sprites(self.user.background.copy(), (self.user.sprite, tuple(self.user.user_pos)))
        else:
            self.user.map_pos[1] += 400
            background = render.get_background(self.user.map_pos, 400)
            self.user.user_pos[1] = 0
            background = render.fill_with_shit(background)
            self.user.background = background.copy()
            background = render.add_dynamic_sprites(background, (self.user.sprite, tuple(self.user.user_pos)))
        return background

# save file with compression
def save_background(image, filename, quality=80):
    image.save(filename, "JPEG", optimize=True, quality=quality)
    image.close()
    return filename
