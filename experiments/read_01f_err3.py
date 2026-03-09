import json
nb_path = r'c:\Users\takahashi\GitHub\molass-researcher\experiments\01_shimizu_averaging\01f_my_my2_baseline_investigation.ipynb'
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    outs = cell.get('outputs', [])
    if not outs:
        continue
    print(f'\n=== Cell {i+1} (exec={cell.get("execution_count")}) ===')
    for out in outs:
        otype = out.get('output_type', '')
        print(f'  output_type: {otype}')
        if otype == 'error':
            print(f'  {out.get("ename")}: {out.get("evalue")}')
            for line in out.get('traceback', [])[-10:]:
                print('  ', line.encode('ascii', errors='replace').decode())
        elif otype == 'stream':
            text = ''.join(out.get('text', []))
            if text.strip():
                print(f'  [{out.get("name")}] {text[:300]}')
        elif otype in ('display_data', 'execute_result'):
            data = out.get('data', {})
            print(f'  mime keys: {list(data.keys())}')
            if 'text/html' in data:
                html = ''.join(data['text/html'])
                print(f'  html snippet: {html[:300]}')
