import json
nb_path = r'c:\Users\takahashi\GitHub\molass-researcher\experiments\01_shimizu_averaging\01f_my_my2_baseline_investigation.ipynb'
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    for out in cell.get('outputs', []):
        if out.get('output_type') == 'error':
            print(f'Cell {i+1}: {out.get("ename")}: {out.get("evalue")}')
            for line in out.get('traceback', [])[-8:]:
                print(line.encode('ascii', errors='replace').decode())
