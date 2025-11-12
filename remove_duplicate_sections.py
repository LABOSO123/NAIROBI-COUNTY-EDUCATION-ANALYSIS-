"""
Remove duplicate sections from the notebook
Keep only the first occurrence of each section header
"""
import json

# Load the notebook
with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

cells = notebook['cells']

# Track seen section headers
seen_headers = set()
cells_to_keep = []
removed_count = 0

for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        
        # Check for section headers (##)
        if source.startswith('##') and not source.startswith('###'):
            header = source.split('\n')[0].strip()
            
            if header in seen_headers:
                print(f"Removing duplicate: Cell {i} - {header[:60]}...")
                removed_count += 1
                continue  # Skip this duplicate
            else:
                seen_headers.add(header)
    
    cells_to_keep.append(cell)

notebook['cells'] = cells_to_keep

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("="*80)
print("DUPLICATE REMOVAL COMPLETE")
print("="*80)
print(f"✓ Removed {removed_count} duplicate section headers")
print(f"✓ Kept {len(cells_to_keep)} cells (was {len(cells)})")
print("\n✅ Notebook cleaned - no more duplicate sections!")


