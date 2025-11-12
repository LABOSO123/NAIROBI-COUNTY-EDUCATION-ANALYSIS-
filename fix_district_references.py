"""
Fix all references to 'District' in recommendations to use 'Constituency' instead
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with recommendations
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'PRIORITY 1: INFRASTRUCTURE CAPACITY BUILDING' in source and "equity_index.head(3)['District']" in source:
        print(f"Found recommendations cell at index {i}")
        
        # Replace District with Constituency
        lines = cell['source']
        new_lines = []
        
        for line in lines:
            # Replace District column reference with Constituency
            if "equity_index.head(3)['District']" in line:
                new_line = line.replace("equity_index.head(3)['District']", "equity_index.head(3)['Constituency']")
                new_line = new_line.replace("top priority districts", "top priority constituencies")
                new_lines.append(new_line)
            # Also replace "districts" with "constituencies" in other places
            elif "districts with zero" in line:
                new_line = line.replace("districts with zero", "constituencies with zero")
                new_lines.append(new_line)
            elif "districts with lowest" in line:
                new_line = line.replace("districts with lowest", "constituencies with lowest")
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        cell['source'] = new_lines
        print("✅ Fixed District references to Constituency")
        break

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook updated successfully")




