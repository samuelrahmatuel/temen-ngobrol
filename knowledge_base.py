import json

def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
