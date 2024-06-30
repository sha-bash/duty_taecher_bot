import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config