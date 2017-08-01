from PIL import Image, ImageDraw

WHITE=(255, 250, 250)
BLACK=(0, 0, 0)
GREEN=(0, 255, 0)
RED=(255, 0, 0)


def draw_hp(percent, player, width=102, height=22):
    hp_bar = Image.new("RGB", (width, height), WHITE)
    drawer = ImageDraw.Draw(hp_bar)
    drawer.rectangle((0, 0, width - 1, height - 1),
                     fill=WHITE, outline=BLACK)
    if player=="this":
        hp_color = GREEN
    elif player=="that":
        hp_color = RED
    else:
        hp_color = None
    drawer.rectangle((1, 1, (width - 1) * percent / 100, height - 2),
                     fill=hp_color)
    return hp_bar


if __name__ == '__main__':
    img1 = draw_hp(80, "this")
    img2 = draw_hp(55, "that")
    img1.save("1.png", "PNG")
    img2.save("2.png", "PNG")
    img1.close()
    img2.close()


