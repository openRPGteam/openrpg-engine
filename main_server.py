import http.server
import engine
import os
import render
from urllib import parse
from random import randint

ACTIVE_USERS = {}
SAVE_DIR = 'serv/'
URL = "http://127.0.0.1:8081/"

def spawn(usrid):
    # create character mover with random skin and random map position
    mv = engine.mover(engine.character('test_resources/hero{}.png'.format(randint(2, 4)),[42 * randint(10, 60), 42 * randint(10, 35)]))
    # add this mover to active users
    ACTIVE_USERS[usrid] = mv
    img = mv.spawn()
    # draw other characters in visible radius
    for idx, usr in ACTIVE_USERS.items():
        if engine.in_vision_field(mv.user.get_pos(), usr.user.get_pos()) and idx != usrid:
            img = render.add_dynamic_sprites(img, (usr.user.sprite, engine.pos_in_vfield(mv, usr)))
    fname = usrid + mv.user.getstrpos() + '.jpg'
    engine.save_background(img, SAVE_DIR + fname)
    return fname

def move(paramlist):
    # obtain mover
    mv = ACTIVE_USERS[paramlist[0]]
    # remove previous image
    os.remove(SAVE_DIR + paramlist[0] + mv.user.getstrpos() + '.jpg')
    back = mv.spawn()
    # move
    if paramlist[1] == '-1':
        back = mv.left()
    elif paramlist[1] == '1':
        back = mv.right()
    if paramlist[2] == '-1':
        back = mv.up()
    elif paramlist[2] == '1':
        back = mv.down()
    # place mover with new position into active users
    ACTIVE_USERS[paramlist[0]] = mv
    # draw other characters in visible radius
    for idx, usr in ACTIVE_USERS.items():
        if engine.in_vision_field(mv.user.get_pos(), usr.user.get_pos()) and idx != paramlist[0]:
            back = render.add_dynamic_sprites(back, (usr.user.sprite, engine.pos_in_vfield(mv, usr)))
    fname = paramlist[0] + mv.user.getstrpos() + '.jpg'
    engine.save_background(back, SAVE_DIR + fname)
    return fname

def end_game(usrid):
    mv = ACTIVE_USERS[usrid]
    del ACTIVE_USERS[usrid]
    os.remove(SAVE_DIR + usrid + mv.user.getstrpos() + '.jpg')
    return "User ended game"


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        path = parse.urlparse(self.path).path[1:]
        # valuelist contains request path, for example [move, 384739, 1, 1]
        valuelist = path.split('/')
        if valuelist[0] == 'spawn':
            response = spawn(valuelist[1])
        elif valuelist[0] == 'move':
            # move needs more than 1 argument
            response = move(valuelist[1:])
        elif valuelist[0] == 'end':
            response = end_game(valuelist[1])
        else:   # if command not supported
            self.send_response(400)
            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Wrong command".encode('utf-8'))
            return
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write((URL + response).encode('utf-8'))


if __name__ == '__main__':
    serv = http.server.HTTPServer(('', 8080), Handler)
    print("serving at port 8080")
    serv.serve_forever()
