from PIL import Image
import os, random

WORLD_MAP = "terrain2.jpg"
SPRITES_DIR = "sprites/"


def get_background(char_pos, size=300):
    """return pure background image around the character in char_pos position."""
    full_back = Image.open(WORLD_MAP).convert("RGBA")
    cropbox = (char_pos[0] - size//2, char_pos[1] - size//2, char_pos[0] + size//2, char_pos[1] + size//2)
    full_back = full_back.crop(cropbox)
    return full_back


def random_pos(image):
    """image must be at least 11x11 px"""
    return (random.randint(0, image.size[0] - 50), random.randint(0, image.size[1] - 50))


def fill_with_shit(background, quantity=random.randint(2,11)):
    """add terrain elements to the background"""
    elements = [SPRITES_DIR + filename for filename in os.listdir(SPRITES_DIR) if filename.endswith('.png')]
    for _ in range(quantity):
        tmpimg = Image.open(elements[random.randint(0, len(elements) - 1)])
        blank = Image.new('RGBA', background.size, color=(0,0,0,0))
        blank.paste(tmpimg, random_pos(background))
        background = Image.alpha_composite(background, blank)
        tmpimg.close(); blank.close()
    return background


def add_dynamic_sprites(terrain_img, spr):
    """sprite list must be a tuple of filename and (x, y) position"""
    transparent = Image.new("RGBA", terrain_img.size, (0,0,0,0))
    tmpimg = Image.open(spr[0]).convert('RGBA')
    transparent.paste(tmpimg, spr[1])
    terrain_img = Image.alpha_composite(terrain_img, transparent)
    tmpimg.close(); transparent.close()
    return terrain_img

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('''Usage: render.py [position x] [position y] [output filename] -s [size] -q [quantity] -d [sprite_list (filename,x,y NO indents)]
        Arguments with switches are optional''')
    else:
        size = int(sys.argv[sys.argv.index('-s') + 1]) if '-s' in sys.argv else 14
        quantity = int(sys.argv[sys.argv.index('-q') + 1]) if '-q' in sys.argv else 10
        bck = get_background((int(sys.argv[1]), int(sys.argv[2])), size)
        bck = fill_with_shit(bck, quantity)
        if '-d' in sys.argv:
            spr_list_begin = sys.argv.index('-d') + 1
            subargv = sys.argv[spr_list_begin:]
            for dyn_sprite in subargv:
                el = dyn_sprite.split(',')
                bck.add_dynamic_sprites((el[0], (int(el[1]), int(el[2]))))
        bck.save(sys.argv[3], "JPEG", optimize=True, quality=80)
        bck.close()
