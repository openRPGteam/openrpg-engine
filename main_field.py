import hp_bars
from PIL import Image

IMG_DIR=""
TEMPBOX=(400,0)


class Player:
    def __init__(self, sprite, hp):
        self.sprite = sprite
        self.hp = hp


def gen_background(this, that):
    bck = Image.open(IMG_DIR + this.sprite)
    enemy = Image.open(IMG_DIR + that.sprite)
    bck.paste(enemy, TEMPBOX)
    enemy.close()
    return bck

def draw_battle(this, that):
    field = gen_background(this, that)
    this_hpbar = hp_bars.draw_hp(this.hp, "this")
    that_hpbar = hp_bars.draw_hp(that.hp, "that")
    field.paste(this_hpbar, (20, 10))
    field.paste(that_hpbar, (478, 10))
    that_hpbar.close()
    this_hpbar.close()
    return field

def save_image(img, path):
    img.save(path, 'JPEG', optimize=True)
    img.close()
    return path.split('/')[-1]



if __name__ == '__main__':
    player1 = Player(IMG_DIR + "hero1.png", 100)
    player2 = Player(IMG_DIR + "enemy1.png", 100)
    for i in range(4):
        tmp = draw_battle(player1, player2)
        tmp.save("bfield{}.png".format(i), "PNG")
        tmp.close()
        if i % 2 == 0:
            player1.hp -= 20
        else:
            player2.hp -= 20