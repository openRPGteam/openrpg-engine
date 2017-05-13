from PIL import Image, ImageDraw

WORLD_MAP = "terrain2.jpg"
SPRITES_DIR = "sprites/"


def get_raw_background(char_pos, size=394):
    """return pure background image around the character in char_pos position."""
    full_back = Image.open(WORLD_MAP).convert("RGBA")
    # get terrain part in radius size/2 from your position
    cropbox = (char_pos[0] - size//2, char_pos[1] - size//2, char_pos[0] + size//2, char_pos[1] + size//2)
    full_back = full_back.crop(cropbox)
    return full_back


def add_dynamic_sprites(terrain_img, spr):
    """sprite list must be a tuple of filename and (x, y) position"""
    transparent = Image.new("RGBA", terrain_img.size, (0,0,0,0))
    tmpimg = Image.open(spr[0]).convert('RGBA')
    transparent.paste(tmpimg, spr[1])
    terrain_img = Image.alpha_composite(terrain_img, transparent)
    tmpimg.close(); transparent.close()
    return terrain_img


def field_markup(background):
    """turn background into 9x9 marked field"""
    # transparent background for markup
    markup = Image.new('RGBA', background.size, (0,0,0,0))
    # draw on markup using drawer
    drawer = ImageDraw.Draw(markup)
    for c in range(1, 9):
        # x0 = (one_column_width + line_width) * line_index
        # y0 = (one_row_height + line_height) * line_index
        x0 = ((background.size[0] - 16) // 9 + 2) * c
        y0 = ((background.size[1] - 16) // 9 + 2) * c
        # draw vertical line where x = x0, color = black, full opacity, thickness = 2
        drawer.line([(x0, 0), (x0, background.size[1])], (0, 0, 0, 255), 2)
        # draw horizontal line where y=y0, color=black, cull opacity, thickness=2
        drawer.line([(0, y0), (background.size[0], y0)], (0, 0, 0, 255), 2)
    # paste markup over background
    background = Image.alpha_composite(background, markup)
    markup.close()
    return background


def draw_map(position, sprite):
    return add_dynamic_sprites(field_markup(get_raw_background(position)), (sprite, (177, 177)))


