import json

# Load notebook
with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with the map save code
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if 'nairobi_map.save' in source and 'Summary statistics' in source:
        # Add display code after the save
        source_lines = cell['source']
        
        # Find the line with the print statement after save
        new_source = []
        for j, line in enumerate(source_lines):
            new_source.append(line)
            if 'print("✅ Saved interactive map' in line:
                # Add display code after this line
                new_source.append('\n')
                new_source.append('# Display map inline in notebook\n')
                new_source.append('print("\\n🗺️  INTERACTIVE MAP:")\n')
                new_source.append('display(nairobi_map)\n')
        
        cell['source'] = new_source
        print(f"✅ Updated cell {i} to display map inline")
        break

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook updated!")




