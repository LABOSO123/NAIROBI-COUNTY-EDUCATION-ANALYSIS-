import json
import os

f1 = 'analysis - New Version.ipynb'
f2 = 'analysis - HUHHH.ipynb'

nb1 = json.load(open(f1, encoding='utf-8'))
nb2 = json.load(open(f2, encoding='utf-8'))

print(f'{f1}:')
print(f'  Cells: {len(nb1["cells"])}')
print(f'  Size: {os.path.getsize(f1):,} bytes')
print(f'  Modified: {os.path.getmtime(f1)}')

print(f'\n{f2}:')
print(f'  Cells: {len(nb2["cells"])}')
print(f'  Size: {os.path.getsize(f2):,} bytes')
print(f'  Modified: {os.path.getmtime(f2)}')




