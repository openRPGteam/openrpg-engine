import http.server
import engine
import os
from urllib import parse

ACTIVE_USERS = {}
SAVE_DIR = 'serv/'
URL = "http://127.0.0.1:8081/"

def spawn(usrid):
    mv = engine.mover(engine.character('test_resources/hero.png'))
    ACTIVE_USERS[usrid] = mv
    fname = usrid + mv.user.getpos() + '.jpg'
    engine.save_background(mv.spawn(),
                           SAVE_DIR + fname)
    return fname

def move(paramlist):
    mv = ACTIVE_USERS[paramlist[0]]
    back = mv.user.background
    os.remove(SAVE_DIR + paramlist[0] + mv.user.getpos() + '.jpg')
    if paramlist[1] == '-1':
        back = mv.left()
    elif paramlist[1] == '1':
        back = mv.right()
    if paramlist[2] == '-1':
        back = mv.up()
    elif paramlist[2] == '1':
        back = mv.down()
    ACTIVE_USERS[paramlist[0]] = mv
    fname = paramlist[0] + mv.user.getpos() + '.jpg'
    engine.save_background(back, SAVE_DIR + fname)
    return fname

def end_game(usrid):
    mv = ACTIVE_USERS[usrid]
    del ACTIVE_USERS[usrid]
    os.remove(SAVE_DIR + usrid + mv.user.getpos() + '.jpg')
    return "User ended game"


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        path = parse.urlparse(self.path).path[1:]
        valuelist = path.split('/')
        if valuelist[0] == 'spawn':
            response = spawn(valuelist[1])
        elif valuelist[0] == 'move':
            response = move(valuelist[1:])
        elif valuelist[0] == 'end':
            response = end_game(valuelist[1])
        else:
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
