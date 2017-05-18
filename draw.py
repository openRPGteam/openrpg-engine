from PIL import Image, ImageDraw


GROUND_TYPES = {
    "MUD" : "sprites/mud.png",
    "GRASS" : "sprites/grass.png",
    "STONE" : "sprites/stone.jpg",
    "EARTH" : "sprites/grass.png"
}

HERO_TYPES = {
    "DISABLED" : "sprites/hero2.png",
    "HIPSTER" : "sprites/hero3.png",
    "ISLAMIC_WARRIOR" : "sprites/hero4.png"
}

MARKUPS = {
    3 : "sprites/3markup.png",
    4 : "sprites/4markup.png",
    9 : "sprites/9markup.png"
}

class draw:
    def __init__(self, size, cell_size):
        transparent_background = Image.new('RGBA',
                                       (size * cell_size, size * cell_size),
                                       (0, 0, 0, 0))
        self.back = transparent_background
        self.size = size
        self.cell_sz = cell_size

    def getsize(self):
        return self.size ** 2

    def set_cell(self, pos, type):
        if type not in GROUND_TYPES.keys() or pos >= self.getsize():
            return False
        x, y = pos % self.size, pos // self.size
        texture = Image.open(GROUND_TYPES[type])
        if texture.size[0] != self.cell_sz:
            texture = texture.resize((self.cell_sz, self.cell_sz))
        self.back.paste(texture, (x * self.cell_sz, y * self.cell_sz))
        texture.close()
        return True

    def draw_transparent(self, pos, tr_type):
        if tr_type not in HERO_TYPES.keys() or pos >= self.getsize():
            return False
        x, y = pos % self.size, pos // self.size
        transparent = Image.new("RGBA", self.back.size, (0, 0, 0, 0))
        hero = Image.open(HERO_TYPES[tr_type]).convert("RGBA")
        if hero.size[0] != self.cell_sz:
            hero = hero.resize((self.cell_sz, self.cell_sz))
        transparent.paste(hero, (x * self.cell_sz, y * self.cell_sz))
        self.back = Image.alpha_composite(self.back, transparent)
        hero.close()
        transparent.close()
        return True

    def add_markup(self, mode):
        if mode not in MARKUPS.keys():
            markup = Image.new('RGBA', self.back.size, (0, 0, 0, 0))
            drawer = ImageDraw.Draw(markup)
            for c in range(1, mode):
                x0 = ((self.back.size[0] - 2 * (mode - 1)) // mode + 2) * c
                y0 = ((self.back.size[1] - 2 * (mode - 1)) // mode + 2) * c
                drawer.line([(x0, 0), (x0, self.back.size[1])], (0, 0, 0, 255), 2)
                drawer.line([(0, y0), (self.back.size[0], y0)], (0, 0, 0, 255), 2)
            fname = 'sprites/{}markup.png'.format(mode)
            markup.save(fname, "PNG")
            MARKUPS[mode] = fname
            self.back = Image.alpha_composite(self.back, markup)
            markup.close()
        else:
            markup = Image.open(MARKUPS[mode])
            self.back = Image.alpha_composite(self.back, markup)
            markup.close()


    def save_image(self, name):
        self.back.save(name, 'JPEG', optimize=True)
        self.back.close()
        return name