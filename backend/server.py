from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse.urlparse(self.path)
        if parsed_url.path == '/search':
            self.do_search()

    def do_search(self):
        parsed_url = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed_url.query)['query'][0]
        print(query)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

print("Server started...")
httpd.serve_forever()
