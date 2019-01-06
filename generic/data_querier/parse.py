import json

class Parser:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.config = json.load(f)

