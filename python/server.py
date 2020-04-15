from http.Server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
import json
from search_engine import SearchEngine


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse.urlparse(self.path)
        if parsed_url.path == '/search':
            self.do_search()

    def do_search(self):
        parsed_url = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed_url.query)['query'][0]

        json_response = SearchEngine.search(query)

        json_response = bytes(json.dumps(json_response), 'utf-8')
        self._set_response()
        self.wfile.write(json_response)


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

print("Server started...")
httpd.serve_forever()
