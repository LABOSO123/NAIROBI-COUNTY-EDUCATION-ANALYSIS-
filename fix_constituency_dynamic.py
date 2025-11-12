"""
Make the recommendations code dynamically use the first column instead of hardcoding 'Constituency'
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with recommendations
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'PRIORITY 1: INFRASTRUCTURE CAPACITY BUILDING' in source:
        print(f"Found recommendations cell at index {i}")
        
        lines = cell['source']
        new_lines = []
        changed = False
        
        for line in lines:
            # Replace hardcoded Constituency with dynamic first column
            if "equity_index.head(3)['Constituency']" in line:
                # Use the first column dynamically
                new_line = line.replace(
                    "equity_index.head(3)['Constituency']",
                    "equity_index.head(3)[equity_index.columns[0]]"
                )
                new_lines.append(new_line)
                changed = True
                print("✅ Made column reference dynamic")
            else:
                new_lines.append(line)
        
        if changed:
            cell['source'] = new_lines
        else:
            print("No changes needed")
        break

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook updated")




