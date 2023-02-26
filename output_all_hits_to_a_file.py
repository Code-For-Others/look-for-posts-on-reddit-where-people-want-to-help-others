import json

with open('storage.json', 'r') as storage_file:
    history = json.load(storage_file)
    hits = []
    for permalink, metadata in history.items():
        if metadata['usefulness'] == 'HIT':
            hits.append(permalink)
    with open('hits.txt', 'w') as hits_file:
        hits_file.write('\n'.join(hits))

