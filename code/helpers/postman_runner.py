import subprocess

class PostmanRunner:
    def __init__(self, collection_file):
        self.collection_file = collection_file

    def run_tests(self):
        command = f"newman run {self.collection_file}"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check the return code to determine if the tests passed or failed
        if result.returncode == 0:
            print("Tests passed!")
        else:
            print("Tests failed!")
        
        # Print the output
        print(result.stdout)
        print(result.stderr)
