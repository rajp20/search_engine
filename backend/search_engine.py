class SearchEngine:
    @staticmethod
    def search(query):
        print("Received query:", query)
        json_response = {
            "result": "hello world"
        }
        return json_response
