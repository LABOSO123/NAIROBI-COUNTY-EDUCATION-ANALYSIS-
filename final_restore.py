import json

print("FINAL RESTORATION - Adding all original cells before census sections")

# Load notebooks
with open('analysis.ipynb', 'r', encoding='utf-8') as f:
    nb_orig = json.load(f)

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb_new = json.load(f)

print(f"Original analysis.ipynb: {len(nb_orig['cells'])} cells")
print(f"Current New Version: {len(nb_new['cells'])} cells")

# Start with ALL original cells
restored_cells = nb_orig['cells'].copy()

# Find insertion point (after PWD section, before "Load Population" or "Composite Equity")
insert_idx = None
for i, cell in enumerate(restored_cells):
    source = ''.join(cell.get('source', []))
    # Look for the cell before "Load Population" or "Composite Equity Index"
    if ('Load Population' in source or 'Composite Equity Index' in source) and '##' in source:
        insert_idx = i
        print(f"Found insertion point at cell {i}: {source[:60]}")
        break

if insert_idx is None:
    # Find after PWD section
    for i, cell in enumerate(restored_cells):
        source = ''.join(cell.get('source', []))
        if 'PWD Capacity Analysis' in source:
            insert_idx = i + 1
            print(f"Found insertion point after PWD at cell {i+1}")
            break

if insert_idx is None:
    insert_idx = 20
    print(f"Using default insertion point: {insert_idx}")

# Get new census sections from New Version
new_sections = []
seen_sources = set()
for cell in nb_new['cells']:
    source = ''.join(cell.get('source', []))
    source_key = source[:100]  # Use first 100 chars as key
    
    # Only add if it's a new census-related section and we haven't seen it
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

print(f"\nFound {len(new_sections)} unique new census sections")

# Insert new sections
for i, new_cell in enumerate(new_sections):
    restored_cells.insert(insert_idx + i, new_cell)

print(f"\n✅ Final cell count: {len(restored_cells)} cells")

# Save
restored_notebook = nb_orig.copy()
restored_notebook['cells'] = restored_cells

with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(restored_notebook, f, indent=1, ensure_ascii=False)

print("✅ RESTORED! All original cells + new census sections")

