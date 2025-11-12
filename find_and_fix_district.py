"""
Find and fix District references in recommendations
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with recommendations
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'PRIORITY 1: INFRASTRUCTURE CAPACITY BUILDING' in source:
        print(f"Found recommendations cell at index {i}")
        
        # Check if it has District reference
        if "equity_index.head(3)['District']" in source:
            print("Found District reference - fixing...")
            lines = cell['source']
            new_lines = []
            
            for line in lines:
                if "equity_index.head(3)['District']" in line:
                    new_line = line.replace("equity_index.head(3)['District']", "equity_index.head(3)['Constituency']")
                    new_line = new_line.replace("top priority districts", "top priority constituencies")
                    new_lines.append(new_line)
                elif "districts with zero" in line:
                    new_line = line.replace("districts with zero", "constituencies with zero")
                    new_lines.append(new_line)
                elif "districts with lowest" in line:
                    new_line = line.replace("districts with lowest", "constituencies with lowest")
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            
            cell['source'] = new_lines
            print("✅ Fixed District references")
        else:
            print("No District reference found - checking for other issues...")
            # Check what column name is actually being used
            if "equity_index.head(3)['Constituency']" in source:
                print("✅ Already using Constituency")
            else:
                print("⚠️  Could not find equity_index reference")
        break

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook check complete")




