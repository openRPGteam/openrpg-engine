from PIL import Image
import os, random

WORLD_MAP = "test_resources/terrain.jpg"
SPRITES_DIR = "test_resources/sprites/"


def get_background(char_pos, size=300):
    """return pure background image around the character in char_pos position."""
    full_back = Image.open(WORLD_MAP).convert("RGBA")
    cropbox = (char_pos[0] - size//2, char_pos[1] - size//2, char_pos[0] + size//2, char_pos[1] + size//2)
    full_back = full_back.crop(cropbox)
    return full_back


def random_pos(image):
    """image must be at least 11x11 px"""
    return (random.randint(0, image.size[0] - 50), random.randint(0, image.size[1] - 50))


def add_dynamic_sprites(terrain_img, spr):
    """sprite list must be a tuple of filename and (x, y) position"""
    transparent = Image.new("RGBA", terrain_img.size, (0,0,0,0))
    tmpimg = Image.open(spr[0]).convert('RGBA')
    transparent.paste(tmpimg, spr[1])
    terrain_img = Image.alpha_composite(terrain_img, transparent)
    tmpimg.close(); transparent.close()
    return terrain_img
