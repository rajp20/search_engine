import subprocess


class MakeSearch:
    java_file = "backend.jar"

    def search(self, query):
        print("Searching...")
        search_result = {}
        output = subprocess.check_output(['java', '-jar', self.java_file, query]).decode('utf-8')
        if "Fail" in output:
            print("Search Failed.")
            search_result["status"] = "Fail"

        print(output)

        print("Done.\n")
        return search_result
