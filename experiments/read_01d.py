import json

nb_path = r'c:\Users\takahashi\GitHub\molass-researcher\experiments\01_shimizu_averaging\01d_my_trimming_investigation.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    outputs = cell.get('outputs', [])
    stdout_lines = []
    for out in outputs:
        if out.get('output_type') == 'stream' and out.get('name') == 'stdout':
            stdout_lines.extend(out.get('text', []))
    if stdout_lines:
        ec = cell.get('execution_count', '?')
        print(f'=== Cell {i+1} (exec {ec}) ===')
        print(''.join(stdout_lines[:80]))
        print()
