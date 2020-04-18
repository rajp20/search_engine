import urllib.parse as urlparse
import subprocess
import json

from http.server import HTTPServer, BaseHTTPRequestHandler

from clustering.Cluster import k_means_pp

print("Loading movie dataset...")
with open('../dataset/movie_reviews.json') as f:
    movie_review_data = json.load(f)
print("Done.\n")


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
        query = urlparse.parse_qs(parsed_url.query)['search_query'][0]

        result_ids = search(query)
        result_data = get_data_from_result_ids(result_ids)

        # BLAZE: Use result_data to do clustering. Call your clustering function here.
        clusters = k_means_pp(result_data, 3, visualize=True)

        json_response = result_data

        json_response = bytes(json.dumps(json_response), 'utf-8')
        self._set_response()
        self.wfile.write(json_response)


def search(query):
    print("Searching...")
    java_file = "GalagoSearch.jar"
    search_result = {}
    output = subprocess.check_output(['java', '-jar', java_file, query]).decode('utf-8')
    if "Fail" in output:
        print("Search Failed.")
        search_result["status"] = "Fail"
    search_result = json.loads(output)
    print("Done.\n")
    return search_result


def get_data_from_result_ids(result_ids):
    print("Getting data from IDs...")
    to_return = {}
    for key in result_ids:
        id_data = movie_review_data[key]
        id_data["Rank"] = result_ids[key]["Rank"]
        id_data["Score"] = result_ids[key]["Score"]
        to_return[key] = id_data
    print("Done.\n")
    return to_return


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

print("Server started...")
httpd.serve_forever()
