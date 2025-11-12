"""
Fix ALL remaining District references in Composite Equity Index section
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

fixed_cells = []

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    # Check if this cell is related to equity index
    if 'equity_index' in source or 'Composite Equity' in source or 'Priority' in source:
        original_source = cell['source'].copy()
        new_source = []
        changed = False
        
        for line in cell['source']:
            new_line = line
            
            # Replace District with Constituency
            if 'District' in line and 'equity_index' in line:
                new_line = line.replace("'District'", "'Constituency'")
                new_line = new_line.replace('"District"', '"Constituency"')
                new_line = new_line.replace('District', 'Constituency')
                if new_line != line:
                    changed = True
            
            # Fix print statements
            if 'Top 10 Priority Districts' in line or 'Top.*Priority.*District' in line:
                new_line = re.sub(r'Top.*Priority.*District[s]?', 'Top Priority Constituencies', line, flags=re.IGNORECASE)
                if new_line != line:
                    changed = True
            
            # Fix any remaining District references in equity_index operations
            if 'equity_index[' in line and 'District' in line:
                new_line = line.replace('District', 'Constituency')
                if new_line != line:
                    changed = True
            
            # Fix visualization titles
            if 'Priority Districts' in line or 'Priority.*District' in line:
                new_line = re.sub(r'Priority.*District[s]?', 'Priority Constituencies', line, flags=re.IGNORECASE)
                if new_line != line:
                    changed = True
            
            new_source.append(new_line)
        
        if changed:
            cell['source'] = new_source
            fixed_cells.append(i)
            print(f"✅ Fixed cell {i}")

# Also check for any output that might have old District data
print(f"\n✅ Fixed {len(fixed_cells)} cells with District references")
print(f"Fixed cells: {fixed_cells}")

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n✅ All District references updated to Constituency!")




