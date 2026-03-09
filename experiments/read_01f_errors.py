import json
nb_path = r'c:\Users\takahashi\GitHub\molass-researcher\experiments\01_shimizu_averaging\01f_my_my2_baseline_investigation.ipynb'
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    for out in cell.get('outputs', []):
        otype = out.get('output_type', '')
        if otype == 'error':
            ename = out.get('ename', '')
            evalue = out.get('evalue', '')
            print(f'Cell {i+1}: {ename}: {evalue}')
            tb = out.get('traceback', [])
            for line in tb[-15:]:
                clean = line.encode('ascii', errors='replace').decode()
                print(clean)
        elif otype == 'stream' and out.get('name') == 'stderr':
            text = ''.join(out.get('text', []))
            if text.strip():
                print(f'Cell {i+1} stderr: {text[:500]}')
