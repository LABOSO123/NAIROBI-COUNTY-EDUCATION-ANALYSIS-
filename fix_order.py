import json

print("FIXING NOTEBOOK ORDER - Title first, then original cells, then census sections")

# Load notebooks
with open('analysis.ipynb', 'r', encoding='utf-8') as f:
    nb_orig = json.load(f)

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb_new = json.load(f)

print(f"Original analysis.ipynb: {len(nb_orig['cells'])} cells")
print(f"Current New Version: {len(nb_new['cells'])} cells")

# Start with ALL original cells from analysis.ipynb (these start with the title)
restored_cells = nb_orig['cells'].copy()

# Find where to insert new census sections - AFTER PWD section, BEFORE "Load Population" or "Composite Equity"
insert_idx = None
for i, cell in enumerate(restored_cells):
    source = ''.join(cell.get('source', []))
    # Look for the markdown cell that says "Load Population" or the section before "Composite Equity Index"
    if ('### Load Population' in source or '## 6. Composite Equity Index' in source) and 'markdown' in str(cell.get('cell_type', '')):
        insert_idx = i
        print(f"Found insertion point at cell {i}: {source[:80]}")
        break

# If not found, look for after PWD Capacity Analysis
if insert_idx is None:
    for i, cell in enumerate(restored_cells):
        source = ''.join(cell.get('source', []))
        if 'PWD Capacity Analysis' in source or 'Estimated PWD capacity gap' in source:
            # Insert after this cell
            insert_idx = i + 1
            print(f"Found insertion point after PWD at cell {i+1}")
            break

if insert_idx is None:
    insert_idx = 20  # Default: after cell 20
    print(f"Using default insertion point: {insert_idx}")

# Get new census sections from New Version (exclude the title/intro cells)
new_sections = []
seen_sources = set()
for cell in nb_new['cells']:
    source = ''.join(cell.get('source', []))
    source_key = source[:150]
    
    # Skip if it's the title or intro
    if 'Nairobi Primary Education Equity Analysis' in source and '## Multi-Dimensional' in source:
        continue
    if 'Table of Contents' in source:
        continue
    
    # Only add if it's a new census-related section
    if source_key not in seen_sources and any(x in source for x in [
        'LOADING ACTUAL CENSUS DATA',
        'GEOGRAPHIC LEVEL EQUITY',
        'School Density vs Population Density',
        'EDUCATION DESERTS',
        'COMPREHENSIVE PRIORITY',
        'LOCATION-LEVEL ANALYSIS',
        'def analyze_by_geographic_level',
        '17 Nairobi Sub-Counties',
        'MAPPING SCHOOLS TO SUB-COUNTIES',
        'MAPPING SUB-COUNTIES TO CONSTITUENCIES'
    ]):
        new_sections.append(cell)
        seen_sources.add(source_key)

print(f"\nFound {len(new_sections)} unique new census sections to insert")

# Insert new sections at the right position
for i, new_cell in enumerate(new_sections):
    restored_cells.insert(insert_idx + i, new_cell)

print(f"\n✅ Final cell count: {len(restored_cells)} cells")
print(f"First cell starts with: {''.join(restored_cells[0].get('source', []))[:60]}")

# Save
restored_notebook = nb_orig.copy()
restored_notebook['cells'] = restored_cells

with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(restored_notebook, f, indent=1, ensure_ascii=False)

print("✅ RESTORED! Title first, then all original cells, then new census sections")




