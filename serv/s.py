import http.server
import socketserver

PORT = 8081

def start():
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()
    return None

if __name__ == '__main__':
    start()
