import http.server
import parse_json
import threading
import os

SAVE_PATH = "serv/"
URL = "http://127.0.0.1:8081/"


def self_destruct_timer(filename, seconds=40.0):
    def rm(path):
        os.remove(path)
        return
    activity = threading.Timer(seconds, rm, args=[SAVE_PATH + filename,] )
    activity.start()
    return filename


class Handler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):

        # send error response
        def err(obj):
            obj.send_response(400)
            obj.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            obj.end_headers()
            obj.wfile.write("Wrong request".encode('utf-8'))
            return

        # send successful response
        def succ(obj, filename):
            obj.send_response(200)
            obj.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            obj.end_headers()
            obj.wfile.write(filename.encode('utf-8'))
            return

        req_data = self.rfile.read(int(self.headers['Content-Length']))

        if self.path.startswith('/battle'):
            # process battle
            req_status = parse_json.check_battle(req_data)
            # check if request is correct
            if req_status[0] == False:
                err(self)
            else:
                # generate image and send response
                img_filename =  self_destruct_timer(parse_json.process_battle(
                    req_status[1], SAVE_PATH) )
                succ(self, URL + img_filename)
        elif self.path.startswith('/map'):
            # process moving on map
            req_status = parse_json.check_request(req_data)
            # check if request is valid
            if req_status[0] == False:
                err(self)
            else:
                # generate image and send response
                img_filename = self_destruct_timer( parse_json.extract_request(
                    req_status[1], SAVE_PATH) )
                succ(self, URL + img_filename.split('/')[-1])
        else:
            err(self)


if __name__ == '__main__':
    serv = http.server.HTTPServer(('', 8080), Handler)
    print("serving at port 8080")
    serv.serve_forever()
