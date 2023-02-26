import json

with open('storage.json', 'r') as storage_file:
    history = json.load(storage_file)
    for permalink, metadata in history.items():
        if (
