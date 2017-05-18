import http.server
import parse_json
import os

LAST_NAME = ""
SAVE_PATH = "serv/"
URL = "http://127.0.0.1:8081/"


class Handler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        global LAST_NAME
        if len(LAST_NAME) > 0:
            os.remove(LAST_NAME)
        req_data = self.rfile.read(int(self.headers['Content-Length']))
        json_req = parse_json.check_request(req_data)
        if json_req[0] == False:
            self.send_response(400)
            self.send_header('Content-Type',
                             'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Wrong request".encode('utf-8'))
            return
        else:
            LAST_NAME = parse_json.extract_request(json_req[1], SAVE_PATH)
            self.send_response(200)
            self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write((URL + LAST_NAME).encode('utf-8'))


if __name__ == '__main__':
    serv = http.server.HTTPServer(('', 8080), Handler)
    print("serving at port 8080")
    serv.serve_forever()
