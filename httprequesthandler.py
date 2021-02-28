import http.server
import socketserver

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/":
            self.path = "/index.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


handler_obj = HttpRequestHandler

PORT = 8000
server = socketserver.TCPServer(("",PORT),handler_obj)
server.serve_forever()
