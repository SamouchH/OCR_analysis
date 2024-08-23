import json

file_path = '../data/processed/annotations/000335_Photo 15-12-2017 12.33.42.txt'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
label = json.loads(content)