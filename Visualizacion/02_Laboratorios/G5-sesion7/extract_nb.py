import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('lab7_clustering.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Print cells 10-22 specifically for DBSCAN part
for i, cell in enumerate(nb['cells']):
    if i < 10 or i > 22:
        continue
    ct = cell['cell_type']
    src = ''.join(cell.get('source', []))
    print(f'=== CELL {i} [{ct}] ===')
    print(src)
    if ct == 'code':
        outputs = cell.get('outputs', [])
        for o in outputs:
            if o.get('output_type') == 'stream':
                print('OUTPUT:', ''.join(o.get('text', [])))
            elif o.get('output_type') in ('display_data', 'execute_result'):
                data = o.get('data', {})
                if 'text/plain' in data:
                    print('OUTPUT (text):', ''.join(data['text/plain']))
    print()
