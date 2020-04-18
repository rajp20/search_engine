import urllib.parse as urlparse
import json
import codecs

from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        parsed_url = urlparse.urlparse(self.path)
        if parsed_url.path == '/cluster':
            self.do_cluster()

    def do_cluster(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        # Use this JSON data to cluster
        data_to_cluster = json.loads(post_data.decode('UTF-8'))

        # Call clustering method here
        json_response = post_data

        # json_response = bytes(json_response, 'utf-8')
        self._set_response()
        self.wfile.write(json_response)


httpd = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)

print("Server started...")
httpd.serve_forever()
