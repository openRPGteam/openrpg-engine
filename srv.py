import engine
import sys
import os

SAVE_DIR='serv/'

if __name__ == '__main__' :
    parsed = list(map(lambda x : int(x), sys.argv[2:-1]))
    if sys.argv[1] == 'spawn' :
        for file in os.listdir('serv') :
            if file.startswith(sys.argv[-1][:-3]):
                os.remove(file)
        mv = engine.mover(engine.character('test_resources/hero.png', [parsed[0], parsed[1]]))
        engine.save_background(mv.spawn(), SAVE_DIR + sys.argv[-1] + '.jpg')
    else:
        for file in os.listdir('serv') :
            if file.startswith(sys.argv[-1][:-3]):
                os.remove(file)
        mv = engine.mover(engine.character('test_resources/hero.png', [parsed[0], parsed[1]], [parsed[2], parsed[3]]))
        back = mv.spawn()
        if parsed[4] == 1:
            back = mv.right()
        elif parsed[4] == -1:
            back = mv.left()
        if parsed[5] == -1:
            back = mv.up()
        elif parsed[5] == 1:
            back = mv.down()
        engine.save_background(back, SAVE_DIR + sys.argv[-1] + '.jpg')
